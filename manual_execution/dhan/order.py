from broker_login.dhan.dhan_api import dhan

def place_order_dhan(security_id, quantity, type="Buy"):
    transaction_type = dhan.BUY
    if type == "Sell":
        transaction_type = dhan.SELL

    try:
        return dhan.place_order(security_id=security_id,  # NiftyPE
                     exchange_segment=dhan.NSE_FNO,
                     transaction_type=transaction_type,
                     quantity=quantity,
                     order_type=dhan.MARKET,
                     product_type=dhan.MARGIN,
                     price=0)
    except Exception as e:
        print(e)