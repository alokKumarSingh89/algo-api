from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from datetime import datetime

from manual_execution.model import PlaceOrderRequest, StrategyList
import dhan_security.helper as helper
from manual_execution.dhan.order import place_order_dhan
from manual_execution.transaction_update import save_data

manual_router: APIRouter = APIRouter(
    prefix="/manual",
    tags=["Manual Run"]
)

pnl = {
    "strategy":[],
    "script":[],
    "expiry":[],
    "date":[],
    "atm": [],
    "atm_id": [],
    "hedge": [],
    "hedge_id": [],
    "quantity":[],
    "transaction_type":[],
    "order":[],
    "position":[]
}


@manual_router.get("")
def welcome():
    return "Hello Manual"

@manual_router.get("/reset")
def reset_pnl():
    global pnl
    if pnl["position"][-1] == 1:
        exit_from_current_postion()
        save_data(pnl)
    pnl = {
        "strategy": [],
        "script": [],
        "expiry": [],
        "date": [],
        "atm": [],
        "atm_id": [],
        "hedge": [],
        "hedge_id": [],
        "quantity":[],
        "transaction_type":[],
        "order": [],
        "position":[]
    }
    return pnl

def update_pnl(body,security):
    global pnl
    pnl["strategy"].append(body["strategy"])
    pnl["script"].append(body["script"])
    pnl["expiry"].append(body["expiry"])
    pnl["atm"].append(security["atm"])
    pnl["atm_id"].append(security["atm_id"])
    pnl["hedge"].append(security["hedge"])
    pnl["hedge_id"].append(security["hedge_id"])
    pnl["date"].append(datetime.now())
    pnl["quantity"].append(security["quantity"])
    return pnl

@manual_router.post("")
def place_order(body: PlaceOrderRequest):
    global pnl
    body = jsonable_encoder(body)
    script = body["script"]
    strategy = body["strategy"]
    expiry = body["expiry"]

    script_fy = helper.get_script_name(script)
    ltp = helper.get_ltp(script_fy)
    if strategy == StrategyList.BullCredit.value:
        security = helper.get_strick(script, expiry, ltp, "PE", -1)
        pnl["transaction_type"].append("Sell")
        pnl["order"].append(-1)
        pnl["position"].append(1)
        place_order_dhan(security["hedge_id"], security["quantity"], "Buy")
        place_order_dhan(security["atm_id"], security["quantity"], "Sell")
        update_pnl(body, security)
        return pnl
    elif strategy == StrategyList.BearCredit.value:
        security = helper.get_strick(script, expiry, ltp, "CE", 1)
        pnl["transaction_type"].append("Sell")
        pnl["order"].append(-1)
        pnl["position"].append(1)
        place_order_dhan(security["hedge_id"], security["quantity"], "Buy")
        place_order_dhan(security["atm_id"], security["quantity"], "Sell")
        update_pnl(body, security)
        return pnl
    elif strategy == StrategyList.BearDebit.value:
        security = helper.get_strick(script, expiry, ltp, "PE", -2)
        update_pnl(body, security)
        return pnl
    elif strategy == StrategyList.BullDebit.value:
        security = helper.get_strick(script, expiry, ltp, "CE", 2)
        update_pnl(body, security)
        return pnl
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not strategy avail for given input')


@manual_router.get("/exit")
def exit_from_current_postion():
    quantity = pnl["quantity"][-1]
    atm_id = pnl["atm_id"][-1]
    order = pnl["order"][-1]
    hedge_id = pnl["hedge_id"][-1]
    position = pnl["position"]
    if position == 0:
        return
    if order == -1:
        place_order_dhan(atm_id, quantity, "Buy")
        place_order_dhan(hedge_id, quantity, "Sell")
    else:
        place_order_dhan(hedge_id, quantity, "Buy")
        place_order_dhan(atm_id, quantity, "Sell")
    pnl["position"][-1] = 0


@manual_router.get("/list")
def get_current_list():
    global pnl
    return pnl

