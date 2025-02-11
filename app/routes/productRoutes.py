from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.productController import delete_product, sync_create_product, sync_update_product


router = APIRouter()

@router.delete("/products/{product_id}", status_code=200)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return delete_product(product_id, db)



# 📌 Endpoint para recibir actualizaciones desde `UpdateProduct`
@router.post("/sync-update")
def sync_product_update(product_data: dict, db: Session = Depends(get_db)):
    return sync_update_product(product_data, db)

@router.post("/sync-create", status_code=200)
def sync_product_create(product_data: dict, db: Session = Depends(get_db)):
    return sync_create_product(product_data, db)
