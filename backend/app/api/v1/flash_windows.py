from fastapi import APIRouter, HTTPException
from app.core.state import state
from app.models.flash_window import FlashWindow

router = APIRouter(
    prefix="/api/flash-windows",
    tags=["flash_windows"],
)


@router.post("/create")
def create_flash_window(window: FlashWindow):
    state.add_flash_window(window)
    return {"status": "ok", "flash_window_id": window.id}


@router.get("/{window_id}")
def get_flash_window(window_id: str):
    window = state.get_flash_window(window_id)
    if not window:
        raise HTTPException(status_code=404, detail="Window not found")
    return window


@router.get("/active/all")
def get_active_windows():
    return state.list_flash_windows_by_status("ACTIVE")


@router.post("/link-precommits")
def link_precommits(payload: dict):
    wid = payload["flash_window_id"]
    sid = payload["seller_id"]
    linked = state.link_precommits_to_window(wid, sid)
    return {"status": "ok", "linked_count": linked}


@router.post("/activate")
def activate_window(payload: dict):
    window_id = payload["flash_window_id"]
    window = state.get_flash_window(window_id)
    if not window:
        raise HTTPException(status_code=404, detail="Window not found")

    window.status = "ACTIVE"
    state.add_flash_window(window)
    return {"status": "ok", "window_id": window_id, "new_status": "ACTIVE"}


from app.core.state import state

@router.get("/debug/precommits")
def debug_precommits():
    """
    DEV ONLY – shows all current precommits in memory
    """
    return {
        "count": len(state.precommits),
        "precommits": state.precommits
    }
