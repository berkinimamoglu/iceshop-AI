class FlashWindow(BaseModel):
    seller_id: str
    product_id: str
    start_time: str
    end_time: str
    expected_buyers: int
    benefit: str | None = None
