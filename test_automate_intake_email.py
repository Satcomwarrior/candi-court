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
    with pytest.raises(FileNotFoundError) as exc_info:
        read_body_template(tmp_path / "missing.txt")
    assert "missing.txt" in str(exc_info.value)


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


def test_group_subject_missing_subject():
    """Test that group_subject handles missing/empty subject properly."""
    # Test with None subject
    with pytest.raises(TypeError) as exc_info:
        group_subject(None, "lawyers")
    assert "subject" in str(exc_info.value).lower()
    
    # Test with empty string subject
    with pytest.raises(ValueError) as exc_info:
        group_subject("", "lawyers")
    assert "empty" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()


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


def test_build_message_unexpected_attachment_types(tmp_path):
    """Test that build_message handles unexpected attachment types properly."""
    # Create a binary file that might cause issues
    binary_file = tmp_path / "test.bin"
    binary_file.write_bytes(b"\x00\x01\x02\x03\xff\xfe\xfd")
    
    # Create a very large filename
    long_name_file = tmp_path / ("a" * 255 + ".txt")
    long_name_file.write_text("content", encoding="utf-8")
    
    recipient = Recipient(name="Bob", email="bob@example.com", rtype="general")
    
    # Test with binary file
    msg1 = build_message(
        "Test Subject",
        "Test Body",
        "Test Sender",
        "test@example.com",
        recipient,
        [binary_file],
    )
    filenames1 = [part.get_filename() for part in msg1.iter_attachments()]
    assert "test.bin" in filenames1
    
    # Test with long filename
    msg2 = build_message(
        "Test Subject", 
        "Test Body",
        "Test Sender",
        "test@example.com",
        recipient,
        [long_name_file],
    )
    filenames2 = [part.get_filename() for part in msg2.iter_attachments()]
    # Should handle long filenames gracefully
    assert len(filenames2) == 1
    
    # Test with non-existent attachment
    non_existent = tmp_path / "does_not_exist.txt"
    with pytest.raises(FileNotFoundError) as exc_info:
        build_message(
            "Test Subject",
            "Test Body", 
            "Test Sender",
            "test@example.com",
            recipient,
            [non_existent],
        )
    assert "does_not_exist.txt" in str(exc_info.value)


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
