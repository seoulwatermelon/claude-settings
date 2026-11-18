"""NAVER WORKS IMAP 접근 — 읽기·첨부 저장·초안 저장만 (발송 없음)."""
import email
import email.header
import email.policy
import html
import imaplib
import os
import re
import time
from contextlib import contextmanager
from email.message import EmailMessage
from email.utils import formatdate, make_msgid, parseaddr
from pathlib import Path

import keyring

import imap_utf7

HOST = os.environ.get("WORKSMAIL_HOST", "imap.worksmobile.com")
PORT = int(os.environ.get("WORKSMAIL_PORT", "993"))
USER = os.environ.get("WORKSMAIL_USER", "seong728@skku.edu")
KEYRING_SERVICE = "worksmail-mcp"
TIMEOUT = 30

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ATTACH_DIR = BASE_DIR / "attachments"
# 첨부 저장을 허용하는 위치(세미콜론 구분). 그 밖은 거부.
ALLOWED_ROOTS = [
    Path(p).resolve()
    for p in os.environ.get(
        "WORKSMAIL_ATTACH_ROOTS",
        rf"E:\SANGSI;C:\Users\SKKU\Downloads\claudecode;{DEFAULT_ATTACH_DIR}",
    ).split(";")
    if p.strip()
]


class MailError(Exception):
    """사용자에게 그대로 보여줄 오류."""


def _password() -> str:
    pw = keyring.get_password(KEYRING_SERVICE, USER)
    if not pw:
        raise MailError(
            "외부 앱 비밀번호가 등록되어 있지 않습니다. set_password.py 를 먼저 실행하세요."
        )
    return pw


@contextmanager
def connect(folder: str | None = None, readonly: bool = True):
    try:
        conn = imaplib.IMAP4_SSL(HOST, PORT, timeout=TIMEOUT)
    except OSError as e:
        raise MailError(f"메일 서버 접속 실패({HOST}:{PORT}): {e}") from e
    try:
        try:
            conn.login(USER, _password())
        except imaplib.IMAP4.error as e:
            raise MailError(f"로그인 실패: 외부 앱 비밀번호를 확인하세요 ({e})") from e
        if folder is not None:
            typ, data = conn.select(_quote(imap_utf7.encode(folder)), readonly=readonly)
            if typ != "OK":
                raise MailError(f"폴더를 열 수 없습니다: {folder} ({data})")
        yield conn
    finally:
        try:
            conn.logout()
        except Exception:
            pass


def _quote(name: str) -> str:
    return '"' + name.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _dh(value) -> str:
    """헤더 디코딩(RFC 2047)."""
    if value is None:
        return ""
    return str(email.header.make_header(email.header.decode_header(str(value))))


# ---------------------------------------------------------------- 폴더

_LIST_RE = re.compile(r'\((?P<flags>[^)]*)\) (?P<delim>"[^"]*"|NIL) (?P<name>.+)')


def list_folders() -> list[dict]:
    with connect() as conn:
        typ, data = conn.list()
    if typ != "OK":
        raise MailError(f"폴더 목록 조회 실패: {data}")
    folders = []
    for raw in data:
        if not raw:
            continue
        m = _LIST_RE.match(raw.decode(errors="replace"))
        if not m:
            continue
        name = m.group("name").strip()
        if name.startswith('"') and name.endswith('"'):
            name = name[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        folders.append({"name": imap_utf7.decode(name), "flags": m.group("flags").split()})
    return folders


def drafts_folder() -> str:
    folders = list_folders()
    for f in folders:
        if "\\Drafts" in f["flags"]:
            return f["name"]
    for f in folders:
        if f["name"].lower() in ("drafts", "임시보관함", "임시 보관함"):
            return f["name"]
    raise MailError("임시보관함 폴더를 찾지 못했습니다. list_folders 결과를 확인하세요.")


# ---------------------------------------------------------------- 검색

def _imap_date(iso: str) -> str:
    try:
        return time.strftime("%d-%b-%Y", time.strptime(iso, "%Y-%m-%d"))
    except ValueError as e:
        raise MailError(f"날짜 형식은 YYYY-MM-DD 입니다: {iso}") from e


def _summary(uid: str, msg) -> dict:
    return {
        "uid": uid,
        "date": _dh(msg.get("Date")),
        "from": _dh(msg.get("From")),
        "to": _dh(msg.get("To")),
        "subject": _dh(msg.get("Subject")),
    }


_UID_RE = re.compile(rb"UID (\d+)")


def _uid_headers(rows):
    """FETCH 응답에서 (uid, header) 쌍. NAVER WORKS는 UID를 리터럴 뒤 별도 줄로 보낸다."""
    pending = None
    for row in rows:
        if isinstance(row, tuple):
            m = _UID_RE.search(row[0])
            if m:
                yield m.group(1).decode(), row[1]
                pending = None
            else:
                pending = row[1]
        elif isinstance(row, bytes) and pending is not None:
            m = _UID_RE.search(row)
            if m:
                yield m.group(1).decode(), pending
            pending = None


def search(folder, sender, subject, text, since, before, limit) -> list[dict]:
    criteria: list[str] = []
    if since:
        criteria += ["SINCE", _imap_date(since)]
    if before:
        criteria += ["BEFORE", _imap_date(before)]
    # 비ASCII 조건은 서버 검색이 불안정하므로 헤더를 받아 직접 거른다.
    local = {}
    for key, val in (("FROM", sender), ("SUBJECT", subject), ("TEXT", text)):
        if not val:
            continue
        if val.isascii():
            criteria += [key, _quote(val)]
        elif key == "TEXT":
            raise MailError("본문(text) 검색은 영문·숫자만 됩니다. 한글은 subject·sender 로 찾으세요.")
        else:
            local[key] = val
    with connect(folder) as conn:
        typ, data = conn.uid("SEARCH", *(criteria or ["ALL"]))
        if typ != "OK":
            raise MailError(f"검색 실패: {data}")
        uids = data[0].split()[::-1]  # 최신 순
        results = []
        for chunk_start in range(0, len(uids), 50):
            chunk = uids[chunk_start:chunk_start + 50]
            typ, rows = conn.uid(
                "FETCH", b",".join(chunk).decode(),
                "(BODY.PEEK[HEADER.FIELDS (DATE FROM TO SUBJECT)])",
            )
            if typ != "OK":
                raise MailError(f"헤더 조회 실패: {rows}")
            for uid, header in _uid_headers(rows):
                s = _summary(uid, email.message_from_bytes(header))
                if "FROM" in local and local["FROM"] not in s["from"]:
                    continue
                if "SUBJECT" in local and local["SUBJECT"] not in s["subject"]:
                    continue
                results.append(s)
            results.sort(key=lambda r: int(r["uid"]), reverse=True)
            if len(results) >= limit:
                break
    return results[:limit]


# ---------------------------------------------------------------- 읽기

def _fetch(conn, uid: str):
    typ, data = conn.uid("FETCH", uid, "(BODY.PEEK[])")
    if typ != "OK" or not data or not isinstance(data[0], tuple):
        raise MailError(f"메일을 찾을 수 없습니다: uid {uid}")
    return email.message_from_bytes(data[0][1], policy=email.policy.default)


def _html_to_text(s: str) -> str:
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\n\s*\n+", "\n\n", html.unescape(s)).strip()


def _attachments(msg) -> list:
    return [p for p in msg.iter_attachments() if p.get_filename()]


def read(folder: str, uid: str, max_chars: int) -> dict:
    with connect(folder) as conn:
        msg = _fetch(conn, uid)
    body_part = msg.get_body(preferencelist=("plain", "html"))
    body = ""
    if body_part is not None:
        body = body_part.get_content()
        if body_part.get_content_type() == "text/html":
            body = _html_to_text(body)
    truncated = len(body) > max_chars
    return {
        **_summary(uid, msg),
        "cc": _dh(msg.get("Cc")),
        "message_id": msg.get("Message-ID", ""),
        "attachments": [
            {"name": p.get_filename(), "type": p.get_content_type(),
             "size": len(p.get_payload(decode=True) or b"")}
            for p in _attachments(msg)
        ],
        "body": body[:max_chars],
        "truncated": truncated,
    }


# ---------------------------------------------------------------- 첨부 저장

def _safe_dir(dest_dir: str | None, uid: str) -> Path:
    target = Path(dest_dir).resolve() if dest_dir else (DEFAULT_ATTACH_DIR / uid).resolve()
    if not any(target == r or r in target.parents for r in ALLOWED_ROOTS):
        allowed = ", ".join(str(r) for r in ALLOWED_ROOTS)
        raise MailError(f"저장 위치가 허용 범위 밖입니다: {target} (허용: {allowed})")
    return target


def _safe_name(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", name).strip(" .")
    return name or "attachment"


def save_attachments(folder: str, uid: str, dest_dir: str | None, names: list[str] | None) -> list[str]:
    target = _safe_dir(dest_dir, uid)
    with connect(folder) as conn:
        msg = _fetch(conn, uid)
    parts = _attachments(msg)
    if names:
        parts = [p for p in parts if p.get_filename() in names]
        if not parts:
            raise MailError(f"이름이 맞는 첨부가 없습니다: {names}")
    target.mkdir(parents=True, exist_ok=True)
    saved = []
    for p in parts:
        path = target / _safe_name(p.get_filename())
        stem, suffix, n = path.stem, path.suffix, 1
        while path.exists():  # 기존 파일 덮어쓰지 않음
            path = target / f"{stem} ({n}){suffix}"
            n += 1
        path.write_bytes(p.get_payload(decode=True) or b"")
        saved.append(str(path))
    return saved


# ---------------------------------------------------------------- 초안

_WEEKDAYS = "월화수목금토일"


def _quote_original(orig) -> str:
    """답장 아래에 붙일 원문 인용(NAVER WORKS 웹메일의 -----Original Message----- 형식)."""
    from email.utils import parsedate_to_datetime
    try:
        d = parsedate_to_datetime(orig.get("Date"))
        sent = f"{d:%Y. %m. %d.} ({_WEEKDAYS[d.weekday()]}) {d:%H:%M}"
    except (TypeError, ValueError):
        sent = _dh(orig.get("Date"))
    part = orig.get_body(preferencelist=("plain", "html"))
    text = ""
    if part is not None:
        text = part.get_content()
        if part.get_content_type() == "text/html":
            text = _html_to_text(text)
    lines = ["", "", "-----Original Message-----",
             f"From: {_dh(orig.get('From'))}", f"To: {_dh(orig.get('To'))}"]
    if orig.get("Cc"):
        lines.append(f"Cc: {_dh(orig.get('Cc'))}")
    lines += [f"Sent: {sent}", f"Subject: {_dh(orig.get('Subject'))}", "",
              text.replace("\r\n", "\n").rstrip()]
    return "\n".join(lines) + "\n"


def save_draft(to: str, subject: str, body: str, cc: str | None,
               reply_folder: str | None, reply_uid: str | None,
               html_body: str | None = None, attach_folder: str | None = None,
               attach_uid: str | None = None, attach_names: list[str] | None = None,
               attach_files: list[str] | None = None) -> dict:
    """html_body 를 주면 text/plain(body) + text/html 두 형식으로 저장한다(서식 유지용).
    attach_uid 를 주면 그 메일의 첨부(attach_names 로 일부 지정)를 그대로 붙인다(디스크 저장 없음)."""
    for addr in [a for a in ((to or "") + "," + (cc or "")).split(",") if a.strip()]:
        if "@" not in parseaddr(addr)[1]:
            raise MailError(f"주소 형식이 아닙니다: {addr}")
    msg = EmailMessage()
    msg["From"] = USER
    if to:
        msg["To"] = to
    if cc:
        msg["Cc"] = cc
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain=USER.split("@")[1])
    if reply_uid:
        with connect(reply_folder or "INBOX") as conn:
            orig = _fetch(conn, reply_uid)
        mid = orig.get("Message-ID")
        if mid:
            msg["In-Reply-To"] = mid
            msg["References"] = (orig.get("References", "") + " " + mid).strip()
        quote = _quote_original(orig)
        body = body.rstrip() + quote
        if html_body:
            html_body += "<br>" + html.escape(quote).replace("\n", "<br>")
    msg.set_content(body, charset="utf-8")
    if html_body:
        msg.add_alternative(html_body, subtype="html", charset="utf-8")
    attached = _copy_attachments(msg, attach_folder, attach_uid, attach_names) if attach_uid else []
    attached += _attach_files(msg, attach_files or [])
    folder = drafts_folder()
    with connect() as conn:
        typ, data = conn.append(
            _quote(imap_utf7.encode(folder)), r"(\Draft \Seen)",
            imaplib.Time2Internaldate(time.time()), msg.as_bytes(),
        )
    if typ != "OK":
        raise MailError(f"초안 저장 실패: {data}")
    return {"folder": folder, "subject": subject, "to": to, "attachments": attached}


MAX_ATTACH_BYTES = 25 * 1024 * 1024


def _attach_files(msg, paths: list[str]) -> list[str]:
    """로컬 파일 첨부. 허용 폴더(ALLOWED_ROOTS) 안의 일반 파일만, 합계 25MB 이하."""
    import mimetypes
    files = []
    for p in paths:
        f = Path(p).resolve()
        if not any(r == f or r in f.parents for r in ALLOWED_ROOTS):
            raise MailError(f"첨부 허용 범위 밖 파일입니다: {f}")
        if not f.is_file():
            raise MailError(f"파일이 없습니다: {f}")
        files.append(f)
    if sum(f.stat().st_size for f in files) > MAX_ATTACH_BYTES:
        raise MailError("첨부 합계가 25MB 를 넘습니다")
    for f in files:
        ctype = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        msg.add_attachment(f.read_bytes(), maintype=maintype, subtype=subtype, filename=f.name)
    return [f.name for f in files]


def _copy_attachments(msg, folder: str | None, uid: str, names: list[str] | None) -> list[str]:
    """다른 메일의 첨부를 초안에 그대로 옮긴다. names 가 하나라도 안 맞으면 오류."""
    with connect(folder or "INBOX") as conn:
        src = _fetch(conn, uid)
    parts = _attachments(src)
    if names:
        missing = [n for n in names if n not in {p.get_filename() for p in parts}]
        if missing:
            raise MailError(f"이름이 맞는 첨부가 없습니다: {missing}")
        parts = [p for p in parts if p.get_filename() in names]
    for p in parts:
        maintype, subtype = p.get_content_type().split("/", 1)
        msg.add_attachment(p.get_payload(decode=True) or b"", maintype=maintype,
                           subtype=subtype, filename=p.get_filename())
    return [p.get_filename() for p in parts]


def delete_draft(uid: str) -> dict:
    """임시보관함의 초안 1통 삭제(다른 폴더는 건드리지 않음)."""
    folder = drafts_folder()
    with connect(folder, readonly=False) as conn:
        typ, data = conn.uid("FETCH", uid, "(FLAGS)")
        if typ != "OK" or not data or data[0] is None:
            raise MailError(f"임시보관함에 없는 메일입니다: uid {uid}")
        conn.uid("STORE", uid, "+FLAGS", r"(\Deleted)")
        conn.expunge()
    return {"deleted": uid, "folder": folder}
