# backend/app/core/state.py

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from app.models.buyer import Buyer
from app.models.seller import Seller
from app.models.flash_window import FlashWindow
from app.models.precommit import PreCommit


class AppState:
    """
    Simple in-memory state holder.
    Faz 3'te DB ile değiştirilecek.
    """

    def __init__(self):
        print("🔥 APPSTATE INSTANCE CREATED:", id(self))
        self.buyers = {}
        self.sellers = {}
        self.products = {}
        self.precommits = {}
        self.flash_windows = {}

    # ---------- BUYERS ----------
    def add_buyer(self, buyer: Buyer) -> Buyer:
        self.buyers[buyer.id] = buyer
        return buyer

    def get_buyer(self, buyer_id: str) -> Optional[Buyer]:
        return self.buyers.get(buyer_id)

    # ---------- SELLERS ----------
    def add_seller(self, seller: Seller) -> Seller:
        self.sellers[seller.id] = seller
        return seller

    def get_seller(self, seller_id: str) -> Optional[Seller]:
        return self.sellers.get(seller_id)

    # ---------- PRECOMMITS ----------
    def add_precommit(
        self,
        buyer_id: str,
        seller_id: str,
        proposed_window_id: str,
        timestamp: Optional[datetime] = None,
    ) -> PreCommit:
        pre_id = str(uuid4())
        pre = PreCommit(
            id=pre_id,
            buyer_id=buyer_id,
            seller_id=seller_id,
            proposed_window_id=proposed_window_id,
            timestamp=timestamp or datetime.utcnow(),
        )
        self.precommits[pre.id] = pre
        return pre

    def get_precommits_for_seller(self, seller_id: str) -> List[PreCommit]:
        return [p for p in self.precommits.values() if p.seller_id == seller_id]

    def get_precommits_for_window(self, proposed_window_id: str) -> List[PreCommit]:
        return [
            p for p in self.precommits.values()
            if p.proposed_window_id == proposed_window_id
        ]

    def link_precommits_to_window(self, flash_window_id: str, seller_id: str):
        window = self.flash_windows.get(flash_window_id)
        if not window:
            return 0

        linked = 0

        for pre in self.precommits.values():
            if (
                pre.seller_id == seller_id
                and pre.proposed_window_id == flash_window_id
            ):
                if pre.id not in window.pre_commit_ids:
                    window.pre_commit_ids.append(pre.id)
                    linked += 1

        return linked

    def get_precommit_buyers_for_window(self, window_id: str) -> List[Buyer]:
        window = self.flash_windows.get(window_id)
        if not window:
            return []
        buyers: List[Buyer] = []
        for pre_id in window.pre_commit_ids:
            pre = self.precommits.get(pre_id)
            if not pre:
                continue
            buyer = self.get_buyer(pre.buyer_id)
            if buyer:
                buyers.append(buyer)
        return buyers

    # ---------- FLASH WINDOWS ----------
    def add_flash_window(self, window: FlashWindow) -> FlashWindow:
        self.flash_windows[window.id] = window
        return window

    def get_flash_window(self, window_id: str) -> Optional[FlashWindow]:
        return self.flash_windows.get(window_id)

    def list_flash_windows_by_status(self, status: str) -> List[FlashWindow]:
        return [w for w in self.flash_windows.values() if w.status == status]

    def join_flash_window(self, buyer_id: str, window_id: str) -> None:
        window = self.flash_windows.get(window_id)
        if not window:
            return

        if buyer_id not in window.participant_ids:
            window.participant_ids.append(buyer_id)
        if buyer_id not in window.buyer_ids:
            window.buyer_ids.append(buyer_id)

        self.flash_windows[window_id] = window

    # ---------- PRODUCTS ----------
    def add_product(self, product: Product) -> Product:
        self.products[product.id] = product
        seller = self.sellers.get(product.seller_id)
        if seller:
            seller.product_ids.append(product.id)
            self.sellers[seller.id] = seller
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

    def get_products_for_seller(self, seller_id: str) -> List[Product]:
        return [p for p in self.products.values() if p.seller_id == seller_id]
        

state = AppState()

