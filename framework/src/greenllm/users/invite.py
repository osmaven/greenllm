
import fcntl
import json
import os
import secrets
import datetime


_DEFAULT_STORE = os.path.join(os.path.expanduser("~"), ".greenllm_invitations.json")


def generate_invitation(email: str, role: str = "student", store_path: str = _DEFAULT_STORE) -> dict:
    """Generate an invitation token for a new user and persist it.

    Args:
        email: The email address of the user to invite.
        role: The role to assign to the user (default: "student").
        store_path: Path to the JSON file used to persist invitations.

    Returns:
        A dict with the invitation details including the token.
    """
    token = secrets.token_urlsafe(32)
    invitation = {
        "email": email,
        "role": role,
        "token": token,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "used": False,
    }
    save_invitation(invitation, store_path=store_path)
    return invitation


def load_invitations(store_path: str = _DEFAULT_STORE) -> list:
    """Load all invitations from the store file.

    Args:
        store_path: Path to the JSON file used to persist invitations.

    Returns:
        A list of invitation dicts.
    """
    if not os.path.exists(store_path):
        return []
    with open(store_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_invitation(invitation: dict, store_path: str = _DEFAULT_STORE) -> None:
    """Append an invitation to the store file.

    Args:
        invitation: The invitation dict to save.
        store_path: Path to the JSON file used to persist invitations.
    """
    with open(store_path, "a+", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.seek(0)
            content = f.read()
            invitations = json.loads(content) if content.strip() else []
            invitations.append(invitation)
            f.seek(0)
            f.truncate()
            json.dump(invitations, f, indent=2, ensure_ascii=False)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
