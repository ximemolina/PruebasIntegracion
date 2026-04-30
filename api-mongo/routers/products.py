from typing import Any
from fastapi import APIRouter, Query, Depends
from controllers.products import ProductsController


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", summary="List products")
def list_products(skip: int = 0, limit: int = 10000) -> Any:
    return ProductsController.get_all_products(skip=skip, limit=limit)

@router.get("/{product_id}", summary="Get product by id")
def get_product(product_id: str) -> Any:
    return ProductsController.get_product_by_id(product_id)
