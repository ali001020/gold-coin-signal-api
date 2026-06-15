from pydantic import BaseModel, Field
from datetime import datetime

class SignalInputSchema(BaseModel):
    gold_price: float= Field(..., gt= 0 ,description= "Gold price")
    coin_price: float= Field(..., gt= 0 ,description= "Coin price")

class SignalOutputSchema(SignalInputSchema):
    id: int= Field(..., description= ("Unique identifier of the signal"))
    signal: str
    created_at: datetime= Field(..., description= "Creation date and time of the signal")