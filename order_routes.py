from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get('')
async def hello_orders():
    return {"message": "Hello Orders"}
