from pydantic import BaseModel, Field
from enum import Enum


class StrategyList(Enum):
    BullCredit = "Bullish Credit"
    BearCredit = "Bear Credit"
    BullDebit = "Bullish Debit"
    BearDebit = "Bear Debit"
    NakedBull = "Naked Bull"
    NakedBear = "Naked Bear"


class PlaceOrderRequest(BaseModel):
    script: str = Field()
    strategy: str = Field(default=StrategyList.BullCredit)
    expiry: str = Field()
