from fastapi import APIRouter, Depends, Path, Query, HTTPException
from tasks.schemas import SignalInputSchema, SignalOutputSchema
from tasks.models import SignalModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List

router= APIRouter(tags= ["signals"])

def get_signal(gold: float, coin: float) -> str:
    if gold > 100 and coin > 50:
        return "Sell"
    elif gold < 80 and coin < 40:
        return "Buy"
    else:
        return"Hold"

@router.get("/")
async def welcome():
    return {"message": "Hello and welcome to signals api."}

@router.get("/signals/history", response_model= List[SignalOutputSchema])
async def signal_histroy(limit: int= 20 ,db: Session= Depends(get_db)):
    
    result= db.query(SignalModel).order_by(SignalModel.id.desc()).limit(limit)
    return result

@router.post("/signals/predict", response_model= SignalOutputSchema)
async def signal_predict(data: SignalInputSchema, db: Session= Depends(get_db)):
    signal= get_signal(data.gold_price, data.coin_price)
    
    new_signal= SignalModel(
        gold_price= data.gold_price,
        coin_price= data.coin_price,
        signal= signal
    )
    
    db.add(new_signal)
    db.commit()
    db.refresh(new_signal)

    return new_signal