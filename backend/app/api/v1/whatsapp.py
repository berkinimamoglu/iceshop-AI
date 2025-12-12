from fastapi import APIRouter
from app.core.state import state

router = APIRouter(
    prefix="/api/whatsapp",
    tags=["whatsapp"],
)

@router.post("/webhook")
def whatsapp_webhook(event: dict):
    text = (event.get("text") or "").lower()
    metadata = event.get("metadata", {})

    buyer_id = metadata.get("buyer_id")
    flash_window_id = metadata.get("flash_window_id")
    seller_id = metadata.get("seller_id")
    proposed_window_id = metadata.get("proposed_window_id")

    if text in ("katıl", "katil", "join", "evet"):

        # ACTIVE WINDOW katılımı
        if flash_window_id:
            state.join_flash_window(buyer_id, flash_window_id)
            return {"status": "ok", "action": "joined_active_window"}

        # PRE-COMMIT
        if buyer_id and seller_id and proposed_window_id:
            pre = state.add_precommit(buyer_id, seller_id, proposed_window_id)
            return {"status": "ok", "action": "precommit_created", "precommit_id": pre.id}

    return {"status": "ignored", "reason": "unsupported_message"}
