"""외부 앱 비밀번호를 Windows 자격 증명 관리자에 저장하고 접속을 확인한다."""
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import keyring  # noqa: E402

import worksmail_imap as mb  # noqa: E402

pw = getpass.getpass(f"{mb.USER} 외부 앱 비밀번호(입력 내용은 보이지 않음): ").strip()
if not pw:
    sys.exit("입력이 비어 있어 저장하지 않았습니다.")
keyring.set_password(mb.KEYRING_SERVICE, mb.USER, pw)
try:
    names = [f["name"] for f in mb.list_folders()]
except mb.MailError as e:
    sys.exit(f"저장은 했지만 접속 확인 실패: {e}")
print("저장·접속 확인 완료. 폴더:", ", ".join(names))
