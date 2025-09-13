import os
from email.message import EmailMessage
from pathlib import Path
from unittest.mock import patch

import pytest

from automation.automate_intake_email import (
    Recipient,
    build_message,
    group_subject,
    load_env,
    read_body_template,
    read_recipients,
    send_messages,
)


def test_load_env_overrides(tmp_path, monkeypatch):
    env_file = tmp_path / "test.env"
    env_file.write_text("FOO=bar\nBAZ=qux\n", encoding="utf-8")
    monkeypatch.setenv("BAZ", "override")
    env = load_env(env_file)
    assert env["FOO"] == "bar"
    assert env["BAZ"] == "override"


def test_read_body_template(tmp_path):
    body_file = tmp_path / "body.txt"
    body_file.write_text("Hello", encoding="utf-8")
    assert read_body_template(body_file) == "Hello"
    with pytest.raises(FileNotFoundError):
        read_body_template(tmp_path / "missing.txt")


def test_read_recipients_dedup(tmp_path):
    csv1 = tmp_path / "recipients.csv"
    csv1.write_text(
        "name,email,type\nAlice,a@example.com,lawyers\nBob,b@example.com,\n",
        encoding="utf-8",
    )
    csv2 = tmp_path / "recipients_forensic.csv"
    csv2.write_text(
        "name,email,type\nBob,b@example.com,\nCarol,c@example.com,\n",
        encoding="utf-8",
    )
    recipients = read_recipients([csv1, csv2])
    emails = {r.email for r in recipients}
    assert emails == {"a@example.com", "b@example.com", "c@example.com"}
    rtypes = {r.email: r.rtype for r in recipients}
    assert rtypes["a@example.com"] == "lawyers"
    assert rtypes["c@example.com"] == "forensic"


def test_group_subject_mapping():
    default = "Default Subject"
    assert group_subject(default, "lawyers") == "Case Intake: Legal Counsel Coordination"
    assert group_subject(default, "unknown") == default


def test_build_message_with_attachment(tmp_path):
    attachment = tmp_path / "file.txt"
    attachment.write_text("data", encoding="utf-8")
    recipient = Recipient(name="Alice", email="alice@example.com", rtype="lawyers")
    msg = build_message(
        "Subject",
        "Body",
        "Sender",
        "sender@example.com",
        recipient,
        [attachment],
    )
    assert msg["From"] == "Sender <sender@example.com>"
    assert msg["To"] == "Alice <alice@example.com>"
    filenames = [part.get_filename() for part in msg.iter_attachments()]
    assert "file.txt" in filenames


def test_send_messages_dry_run(capsys):
    env = {"SMTP_HOST": "smtp.test", "SMTP_PORT": "587", "SMTP_USER": "user"}
    msg = EmailMessage()
    msg.set_content("hi")
    send_messages(env, [msg], dry_run=True)
    captured = capsys.readouterr()
    assert "Would send 1 messages" in captured.out


def test_send_messages_real():
    env = {
        "SMTP_HOST": "smtp.test",
        "SMTP_PORT": "587",
        "SMTP_USER": "user",
        "SMTP_PASS": "pass",
    }
    msg = EmailMessage()
    msg.set_content("hi")
    with patch("smtplib.SMTP") as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value
        send_messages(env, [msg], dry_run=False)
        mock_smtp.assert_called_with("smtp.test", 587)
        instance.starttls.assert_called_once()
        instance.login.assert_called_once_with("user", "pass")
        instance.send_message.assert_called_once_with(msg)
