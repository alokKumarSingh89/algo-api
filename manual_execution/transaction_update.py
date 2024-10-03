import pandas as pd
def save_data(pnl):
    df = pd.DataFrame(pnl)
    df.to_csv("pnl.csv", mode="a")