from sqlalchemy.orm import Session
from app.models.product import Product
import os
import requests

# 🔥 URLs de los microservicios `CreateProduct`, `ReadProduct` y `UpdateProduct`
CREATE_PRODUCT_SERVICE_URL = os.getenv("CREATE_PRODUCT_SERVICE_URL", "http://localhost:8000")
READ_PRODUCT_SERVICE_URL = os.getenv("READ_PRODUCT_SERVICE_URL", "http://localhost:8002")
UPDATE_PRODUCT_SERVICE_URL = os.getenv("UPDATE_PRODUCT_SERVICE_URL", "http://localhost:8003")

def delete_product(product_id: int, db: Session):
    """Elimina un producto en `DeleteProduct` y lo sincroniza con los demás microservicios"""

    # Buscar el producto en la base de datos
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return {"error": "Producto no encontrado en DeleteProduct"}

    # Eliminar el producto de la base de datos
    db.delete(db_product)
    db.commit()

    print(f"✅ Producto eliminado en DeleteProduct: {product_id}")

    # 🔄 Sincronizar la eliminación con los demás microservicios
    sync_delete_with_microservices(product_id)

    return {"message": "Producto eliminado correctamente"}

def sync_delete_with_microservices(product_id: int):
    """ 🔄 Notificar a `CreateProduct`, `ReadProduct` y `UpdateProduct` que eliminen el producto """
    
    sync_services = [
        f"{CREATE_PRODUCT_SERVICE_URL}/sync-delete",
        f"{READ_PRODUCT_SERVICE_URL}/sync-delete",
        f"{UPDATE_PRODUCT_SERVICE_URL}/sync-delete"
    ]

    data = {"id": product_id}

    for service in sync_services:
        try:
            response = requests.post(service, json=data)
            if response.status_code == 200:
                print(f"✅ Producto eliminado correctamente en {service}")
            else:
                print(f"⚠️ Error eliminando en {service}. Código: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error enviando solicitud a {service}: {e}")

def sync_create_product(product_data: dict, db: Session):
    """ 📌 Sincronizar un producto creado en `CreateProduct` """
    
    db_product = Product(
        id=product_data["id"],  
        nombreProducto=product_data["nombreProducto"],
        descripcion=product_data["descripcion"],
        marca=product_data["marca"],
        precio=product_data["precio"],
        proveedor_id=product_data["proveedor_id"],
        proveedor_nombre=product_data["proveedor_nombre"],
    )

    # 🔥 Verificar si el producto ya existe antes de insertarlo
    existing_product = db.query(Product).filter(Product.id == db_product.id).first()
    if existing_product:
        print(f"⚠️ Producto con ID {db_product.id} ya existe en DeleteProduct.")
        return

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    print(f"✅ Producto sincronizado en DeleteProduct: {db_product.nombreProducto}")
    return db_product
