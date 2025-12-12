from fastapi import APIRouter, HTTPException
from typing import List

from app.core.state import state
from app.models.seller import Seller
from app.models.product import Product

router = APIRouter(
    prefix="/api/sellers",
    tags=["sellers"],
)


# --------------------------
#  SELLER REGISTRATION
# --------------------------

@router.post("/register")
def register_seller(seller: Seller):
    """
    Registers a new seller into the system.
    """
    state.add_seller(seller)
    return {"status": "ok", "seller_id": seller.id}


# --------------------------
#  GET SELLER INFO
# --------------------------

@router.get("/{seller_id}")
def get_seller(seller_id: str):
    seller = state.get_seller(seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller


# --------------------------
#  ADD PRODUCT TO SELLER
# --------------------------

@router.post("/{seller_id}/products")
def add_product_to_seller(
    seller_id: str,
    payload: dict
):
    """
    Adds a product to a seller's product list.
    Expected payload: { "name": "...", "category": "...", "price": 10.0, "stock": 20 }
    """

    seller = state.get_seller(seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    product = Product(
        id=f"prod_{seller_id}_{len(seller.product_ids) + 1}",
        seller_id=seller_id,
        name=payload.get("name"),
        category=payload.get("category"),
        price=payload.get("price"),
        stock=payload.get("stock"),
    )

    state.add_product(product)

    return {
        "status": "ok",
        "product": product
    }


# --------------------------
#  LIST PRODUCTS OF SELLER
# --------------------------

@router.get("/{seller_id}/products")
def list_seller_products(seller_id: str) -> List[Product]:
    seller = state.get_seller(seller_id)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    return state.get_products_for_seller(seller_id)
