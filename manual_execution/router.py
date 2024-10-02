from fastapi import APIRouter

from manual_execution.model import PlaceOrderRequest

manual_router: APIRouter = APIRouter(
    prefix="/manul",
    tags=["Manul Run"]
)


@manual_router.get("")
def welcome():
    return "Hello Manual"


@manual_router.post("")
def place_order(body: PlaceOrderRequest):
    return body
