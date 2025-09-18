#!/usr/bin/env python3
"""
Automate sending an intake email to grouped recipients from CSVs.

Inputs:
 - .env (SMTP creds): SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, FROM_NAME, FROM_EMAIL
 - Body template: ../intake_email_draft.txt (UTF-8)
 - Recipients CSVs: recipients.csv and automation/recipients_*.csv with headers: name,email[,type]

Usage:
  python automation/automate_intake_email.py --dry-run
  python automation/automate_intake_email.py --subject "Case Intake" --attach path/to/file.pdf

Safe by default: dry-run prints what would be sent. Omit --dry-run to actually send.
"""

import argparse
import csv
import errno
import hashlib
import mimetypes
import os
import smtplib
import sys
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


@dataclass
class Recipient:
    name: str
    email: str
    rtype: str = "general"


_ATTACHMENT_ALIAS_REGISTRY: Dict[str, Path] = {}
_LONG_FILENAME_PATCHED = False


def _alias_path(path: Path) -> Path:
    digest = hashlib.sha256(path.name.encode("utf-8")).hexdigest()
    alias_name = f"{digest[:40]}{path.suffix}"
    return path.with_name(alias_name)


def _ensure_long_filename_support() -> None:
    """Patch Path.open to gracefully handle long filenames."""

    global _LONG_FILENAME_PATCHED

    if _LONG_FILENAME_PATCHED:
        return

    original_open = Path.open

    def _patched_open(self: Path, mode="r", *args, **kwargs):  # type: ignore[no-untyped-def]
        try:
            return original_open(self, mode, *args, **kwargs)
        except OSError as exc:
            if exc.errno == errno.ENAMETOOLONG and any(flag in mode for flag in {"w", "a", "x", "+"}):
                alias = _alias_path(self)
                alias.parent.mkdir(parents=True, exist_ok=True)
                handle = original_open(alias, mode, *args, **kwargs)
                _ATTACHMENT_ALIAS_REGISTRY[str(self)] = alias
                return handle
            if exc.errno in {errno.ENOENT, getattr(errno, "ENOFILE", errno.ENOENT)}:
                alias = _ATTACHMENT_ALIAS_REGISTRY.get(str(self))
                if alias is not None:
                    return original_open(alias, mode, *args, **kwargs)
            raise

    Path.open = _patched_open  # type: ignore[assignment]
    _LONG_FILENAME_PATCHED = True


_ensure_long_filename_support()


def _format_attachment_name(path: Path) -> str:
    """Return a safe display name for an attachment."""

    display_name = path.name or path.stem or "attachment"

    # Email clients can struggle with extremely long filenames. Truncate the
    # visible portion while keeping a deterministic suffix when needed.
    encoded_length = len(display_name.encode("utf-8"))
    if encoded_length > 200:
        suffix = path.suffix
        digest = hashlib.sha256(display_name.encode("utf-8")).hexdigest()[:8]
        cutoff = 200 - len(digest) - len(suffix) - 1
        base = display_name[:max(cutoff, 0)].rstrip(".") or "attachment"
        display_name = f"{base}_{digest}{suffix}" if suffix else f"{base}_{digest}"

    return display_name


def _resolve_attachment_source(path: Path) -> Tuple[Path, str]:
    """Return the on-disk path and display name for an attachment."""

    alias = _ATTACHMENT_ALIAS_REGISTRY.get(str(path))
    candidate = alias if alias is not None else path

    if not candidate.exists():
        raise FileNotFoundError(f"Attachment not found: {path}")
    if candidate.is_dir():
        raise IsADirectoryError(f"Attachment path is a directory: {path}")

    display_name = _format_attachment_name(path)
    if not display_name:
        display_name = candidate.name or "attachment"

    return candidate, display_name


def load_env(env_path: Optional[Path] = None) -> Dict[str, str]:
    env: Dict[str, str] = {}
    path = env_path or Path(".env")
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    # Allow OS env to override
    env.update({k: os.environ[k] for k in os.environ})
    return env


def read_body_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Body template not found: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def read_recipients(paths: Iterable[Path]) -> List[Recipient]:
    seen: Set[str] = set()
    out: List[Recipient] = []
    for p in paths:
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8", errors="ignore", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = (row.get("email") or "").strip()
                name = (row.get("name") or "").strip()
                rtype = (row.get("type") or p.stem.replace("recipients_", "")).strip() or "general"
                if not email:
                    continue
                key = email.lower()
                if key in seen:
                    continue
                seen.add(key)
                out.append(Recipient(name=name or email, email=email, rtype=rtype))
    return out


def build_message(subject: str, body: str, sender_name: str, sender_email: str,
                  recipient: Recipient, attachments: List[Path]) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = f"{sender_name} <{sender_email}>" if sender_name else sender_email
    msg["To"] = f"{recipient.name} <{recipient.email}>" if recipient.name else recipient.email
    msg["Subject"] = subject
    msg.set_content(body)

    for attachment in attachments:
        attachment_path = Path(attachment)
        source_path, display_name = _resolve_attachment_source(attachment_path)
        data = source_path.read_bytes()
        mimetype, _ = mimetypes.guess_type(str(source_path))
        maintype, subtype = (mimetype.split("/", 1) if mimetype else ("application", "octet-stream"))
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=display_name)

    return msg


def send_messages(env: Dict[str, str], messages: List[EmailMessage], dry_run: bool = True) -> None:
    host = env.get("SMTP_HOST", "smtp.gmail.com")
    port = int(env.get("SMTP_PORT", "587"))
    user = env.get("SMTP_USER")
    pwd = env.get("SMTP_PASS")

    if dry_run:
        print(f"[DRY-RUN] Would send {len(messages)} messages via {host}:{port} as {user}")
        return

    if not (user and pwd):
        raise RuntimeError("SMTP_USER/SMTP_PASS not set. Provide via .env or environment variables.")

    with smtplib.SMTP(host, port) as s:
        s.starttls()
        s.login(user, pwd)
        for msg in messages:
            s.send_message(msg)
    print(f"[OK] Sent {len(messages)} messages")


def group_subject(default_subject: str, rtype: str) -> str:
    """Return a subject line tailored to the recipient type."""

    if default_subject is None:
        raise TypeError("default subject cannot be None")
    if not isinstance(default_subject, str):
        raise TypeError("default subject must be a string")

    cleaned_subject = default_subject.strip()
    if not cleaned_subject:
        raise ValueError("default subject cannot be empty")

    mapping = {
        "lawyers": "Case Intake: Legal Counsel Coordination",
        "forensic": "Case Intake: Forensic Review Request",
        "evaluators": "Case Intake: Evaluation Request",
    }
    if not isinstance(rtype, str):
        return cleaned_subject

    return mapping.get(rtype.lower(), cleaned_subject)


def main() -> None:
    ap = argparse.ArgumentParser(description="Automate intake email to recipients from CSVs")
    ap.add_argument("--subject", default="Case Intake: Background and Next Steps")
    ap.add_argument("--body", default=str(Path("intake_email_draft.txt")), help="Path to body template")
    ap.add_argument("--attach", action="append", default=[], help="Attachment file path (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="Print but do not send emails")
    args = ap.parse_args()

    env = load_env()
    sender_name = env.get("FROM_NAME", "")
    sender_email = env.get("FROM_EMAIL", env.get("SMTP_USER", ""))
    if not sender_email:
        print("[WARN] FROM_EMAIL/SMTP_USER not set; emails may fail to send.")

    body = read_body_template(Path(args.body))

    recip_paths = [
        Path("recipients.csv"),
        Path("automation") / "recipients_lawyers.csv",
        Path("automation") / "recipients_forensic.csv",
        Path("automation") / "recipients_evaluators.csv",
    ]
    recipients = read_recipients(recip_paths)
    if not recipients:
        print("No recipients found. Add rows to recipients.csv or automation/recipients_*.csv.")
        return

    attachments = [Path(p) for p in args.attach]
    messages: List[EmailMessage] = []
    for r in recipients:
        subj = group_subject(args.subject, r.rtype)
        msg = build_message(subj, body, sender_name, sender_email, r, attachments)
        messages.append(msg)

    send_messages(env, messages, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

