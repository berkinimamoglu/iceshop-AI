from typing import List

class Seller(BaseModel):
    id: str
    phone_number: str
    name: str
    category: str
    location: Location
    density_status: Optional[str] = None
    stock_status: Optional[str] = None
    product_ids: List[str] = []   # 🔥 ürün referansları buraya


@router.post("/{seller_id}/products")
def add_product(seller_id: str, payload: ProductCreatePayload):
    product = Product(
        id=str(uuid4()),
        seller_id=seller_id,
        name=payload.name,
        category=payload.category,
        price=payload.price,
        stock=payload.stock
    )
    state.add_product(product)
    return {"status": "ok", "product": product}


class ProductCreatePayload(BaseModel):
    name: str
    category: Optional[str]
    price: float
    stock: Optional[int]
uvicorn app.main:app --reload
