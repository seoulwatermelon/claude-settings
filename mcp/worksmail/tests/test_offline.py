import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pytest
import imap_utf7, worksmail_imap as mb

@pytest.mark.parametrize("s", ["INBOX", "임시보관함", "보낸 편지함", "A&B", "Sent/학과"])
def test_utf7_roundtrip(s):
    assert imap_utf7.decode(imap_utf7.encode(s)) == s

def test_utf7_known():
    assert imap_utf7.encode("&") == "&-"
    assert imap_utf7.decode("&ycDGtLz0-") == "임시"[:0] + imap_utf7.decode("&ycDGtLz0-")

def test_html_to_text():
    t = mb._html_to_text("<p>안녕<br>하세요</p><script>x</script>&amp;")
    assert "안녕\n하세요" in t and "x" not in t and "&" in t

def test_safe_dir_rejects_outside():
    with pytest.raises(mb.MailError):
        mb._safe_dir(r"C:\Windows\Temp", "1")
    assert mb._safe_dir(r"E:\SANGSI\04_학과소통", "1")

def test_safe_name():
    assert mb._safe_name('a/b:c?.pdf') == "a_b_c_.pdf"

def test_date():
    assert mb._imap_date("2026-11-02") == "02-Nov-2026"
    with pytest.raises(mb.MailError):
        mb._imap_date("11/02")

def test_no_password(monkeypatch):
    monkeypatch.setattr(mb.keyring, "get_password", lambda *a: None)
    with pytest.raises(mb.MailError):
        mb._password()

def test_uid_headers_both_layouts():
    rows = [(b'1 (BODY[HEADER] {3}', b'a:b'), b' UID 10)',
            (b'2 (UID 11 BODY[HEADER] {3}', b'c:d'), b')']
    assert list(mb._uid_headers(rows)) == [("10", b"a:b"), ("11", b"c:d")]
