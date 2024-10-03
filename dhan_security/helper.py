import requests
import pandas as pd
import os
script_list = {
    "MIDCPNIFTY": {"name": "NSE:MIDCPNIFTY-INDEX", "lots":50,"stick_diff":25},
    "FINNIFTY": {"name":"NSE:FINNIFTY-INDEX", "lots":25,"stick_diff":50},
    "NIFTYBANK": {"name":"NSE:NIFTYBANK-INDEX", "lots":15,"stick_diff":100},
    "NIFTY50": {"name":"NSE:NIFTY50-INDEX", "lots":25,"stick_diff":50}
}
qunatity = 1
csv = pd.read_csv(os.path.dirname(__file__)+"/api-scrip-master.csv")

def get_script_name(script):
    return script_list[script]["name"]


def get_ltp(script: str):
    res = requests.get(f'http://127.0.0.1:5100/ltp/{script}')
    return res.json()


# get dhan security id
def get_strick(script, expiry, ltp, option_type, diff):
    script_config = script_list[script]
    atm  =  (ltp//script_config["stick_diff"])*script_config["stick_diff"]
    hedge = atm + (diff*script_config["stick_diff"])
    NSE_CSV = csv[csv["SEM_EXM_EXCH_ID"] == 'NSE']
    NSE_CSV = NSE_CSV[NSE_CSV["SEM_INSTRUMENT_NAME"] == "OPTIDX"]
    NSE_CSV = NSE_CSV[NSE_CSV["SEM_OPTION_TYPE"] == option_type]
    NSE_CSV = NSE_CSV[NSE_CSV["SEM_EXPIRY_DATE"].str.contains(expiry)]
    atm_id = NSE_CSV[NSE_CSV["SEM_STRIKE_PRICE"] == atm]["SEM_SMST_SECURITY_ID"].to_list()[0]
    hedge_id = NSE_CSV[NSE_CSV["SEM_STRIKE_PRICE"] == hedge]["SEM_SMST_SECURITY_ID"].to_list()[0]
    return {"atm_id":str(atm_id), "hedge_id":str(hedge_id), "atm":atm, "hedge":hedge, "quantity":qunatity*script_config["lots"]}