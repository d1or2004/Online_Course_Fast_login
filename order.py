from fastapi import APIRouter

order_rooter = APIRouter(prefix="/order")


@order_rooter.get('/')
async def order():
    return {"massage": "Order rooter"}
