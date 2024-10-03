from fastapi import FastAPI, BackgroundTasks
import uvicorn
from fyers_apiv3.FyersWebsocket import data_ws


from broker_login.fyers.fyers import Fyers
login = Fyers()
from datetime import datetime

app = FastAPI(title="Trading App Socket")


ltp_list = {

}
time_frame_data = {

}
key = None
fyers = None
def subscribe(list):
    global sticke_ltp, time_frame_data
    for symbol in list:
        time_frame_data[symbol] = {
            "open":[],
            "close":[],
            "high":[],
            "low":[],
            "date":[],
            "volumn":[]
        }

    def onmessage(message):
        global key
        if message.get("ltp") is not None:
            script_symbol = message.get("symbol")
            if message.get('last_traded_time') is not None:
                last_traded_time = message.get('last_traded_time')
                last_traded_date = datetime.fromtimestamp(last_traded_time).strftime('%d-%m-%y %H:%M:%S')
                time_frame_data[script_symbol]["date"].append(last_traded_date)
            if message.get("exch_feed_time"):
                last_traded_time = message.get('exch_feed_time')
                last_traded_date = datetime.fromtimestamp(last_traded_time).strftime('%d-%m-%y %H:%M:%S')
                time_frame_data[script_symbol]["date"].append(last_traded_date)
            ltp = message.get('ltp')
            vol_traded_today = message.get("vol_traded_today") or 0
            time_frame_data[script_symbol]["open"].append(ltp)
            time_frame_data[script_symbol]["close"].append(ltp)
            time_frame_data[script_symbol]["high"].append(ltp)
            time_frame_data[script_symbol]["low"].append(ltp)
            time_frame_data[script_symbol]["volumn"].append(vol_traded_today)
        print("Response:", ltp, script_symbol)

    def onerror(message):
        print("Error:", message)

    def onclose(message):
        print("Connection closed:", message)

    def onopen():
        data_type = "SymbolUpdate"  #"SymbolUpdate"
        fyers.subscribe(symbols=list, data_type=data_type)

        # Keep the socket running to receive real-time data
        fyers.keep_running()

    global fyers
    fyers = data_ws.FyersDataSocket(
        access_token=login.get_save_token(),  # Access token in the format "appid:accesstoken"
        log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
        litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
        write_to_file=False,  # Save response in a log file instead of printing it.
        reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
        on_connect=onopen,  # Callback function to subscribe to data upon connection.
        on_close=onclose,  # Callback function to handle WebSocket connection close events.
        on_error=onerror,  # Callback function to handle WebSocket errors.
        on_message=onmessage  # Callback function to handle incoming messages from the WebSocket.
    )

    # Establish a connection to the Fyers WebSocket
    fyers.connect()


def disconnect():
    global fyers, time_frame_data,ltp_list
    time_frame_data = {}
    ltp_list = {}
    if fyers is not None and fyers.is_connected():
        fyers.close_connection()

def get_script_list():
    instrument_list: list = ["NSE:NIFTYBANK-INDEX","NSE:NIFTY50-INDEX"]
    return instrument_list

@app.get("/")
def socket_health():
    return {"Name": "Socket Running"}

@app.get("/start-broker")
def start_broker_to_subscribe_script(background_task: BackgroundTasks):
    disconnect()
    scripts = get_script_list()
    background_task.add_task(subscribe, scripts)
    return "success"

@app.get("/script/{script_name}")
def get_lpt_detail(script_name: str):
    print(time_frame_data.get(script_name), time_frame_data)
    return time_frame_data.get(script_name) or -1

@app.get("/ltp/{script_name}")
def get_lpt_detail(script_name: str):
    if time_frame_data.get(script_name):
        return time_frame_data.get(script_name)["close"][-1] or -1
    return -1

if __name__ == '__main__':
    uvicorn.run(app="web_socket:app", port=5100, log_level="info", reload=False)
    print("dssd")