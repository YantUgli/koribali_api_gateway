import json
from pathlib import Path

# Load sekali saat startup, tidak perlu baca file tiap request
_MESSAGES_PATH = Path(__file__).parent / "messages.json"
_messages = json.loads(_MESSAGES_PATH.read_text(encoding="utf-8"))

DEFAULT_SUCCESS_MESSAGE: str = _messages["default_success_message"]
UNIQUE_CODE_MESSAGES: dict[str, str] = _messages["unique_codes"]

def get_message_by_unique_code(unique_code: int | None) -> str:
    if unique_code is None:
        return DEFAULT_SUCCESS_MESSAGE
    return UNIQUE_CODE_MESSAGES.get(str(unique_code), DEFAULT_SUCCESS_MESSAGE)