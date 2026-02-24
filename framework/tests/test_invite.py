
import json
import os
import pytest
from greenllm.users.invite import generate_invitation, load_invitations, save_invitation


@pytest.fixture
def tmp_store(tmp_path):
    return str(tmp_path / "invitations.json")


def test_generate_invitation_returns_required_fields(tmp_store):
    inv = generate_invitation("alice@example.com", store_path=tmp_store)
    assert inv["email"] == "alice@example.com"
    assert inv["role"] == "student"
    assert "token" in inv
    assert len(inv["token"]) > 0
    assert "created_at" in inv
    assert inv["used"] is False


def test_generate_invitation_default_role(tmp_store):
    inv = generate_invitation("bob@example.com", store_path=tmp_store)
    assert inv["role"] == "student"


def test_generate_invitation_custom_role(tmp_store):
    inv = generate_invitation("prof@example.com", role="instructor", store_path=tmp_store)
    assert inv["role"] == "instructor"


def test_generate_invitation_unique_tokens(tmp_store):
    inv1 = generate_invitation("user1@example.com", store_path=tmp_store)
    inv2 = generate_invitation("user2@example.com", store_path=tmp_store)
    assert inv1["token"] != inv2["token"]


def test_invitation_persisted(tmp_store):
    generate_invitation("carol@example.com", store_path=tmp_store)
    invitations = load_invitations(store_path=tmp_store)
    assert len(invitations) == 1
    assert invitations[0]["email"] == "carol@example.com"


def test_load_invitations_empty_when_no_store(tmp_store):
    invitations = load_invitations(store_path=tmp_store)
    assert invitations == []


def test_multiple_invitations_accumulate(tmp_store):
    generate_invitation("user1@example.com", store_path=tmp_store)
    generate_invitation("user2@example.com", store_path=tmp_store)
    invitations = load_invitations(store_path=tmp_store)
    assert len(invitations) == 2
    emails = {i["email"] for i in invitations}
    assert emails == {"user1@example.com", "user2@example.com"}


def test_save_invitation_writes_json(tmp_store):
    invitation = {
        "email": "dave@example.com",
        "role": "admin",
        "token": "testtoken123",
        "created_at": "2026-01-01T00:00:00",
        "used": False,
    }
    save_invitation(invitation, store_path=tmp_store)
    with open(tmp_store, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["token"] == "testtoken123"
