from fastapi import APIRouter, Depends, Path, Query, HTTPException
from tasks.schemas import SignalInputSchema, SignalOutputSchema
from tasks.models import SignalModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import ollama

router= APIRouter(tags= ["signals"])

def get_signal_with_llm(gold: float, coin: float) -> str:
    
    prompt = f"""Based on gold price = {gold} and coin price = {coin}, 
    decide if the user should Buy, Sell, or Hold. 
    Answer with only one word: Buy, Sell, or Hold."""
    
    try:
        response = ollama.chat(
            model='llama3.2:latest',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0}
        )
        signal = response['message']['content'].strip()
        
        if "Buy" in signal:
            return "Buy"
        elif "Sell" in signal:
            return "Sell"
        else:
            return "Hold"
            
    except Exception as e:
        print(f"Ollama error: {e}")
        return "Hold"

    
@router.get("/")
async def welcome():
    return {"message": "Hello and welcome to signals api."}

@router.get("/signals/history", response_model= List[SignalOutputSchema])
async def signal_histroy(limit: int= 20 ,db: Session= Depends(get_db)):
    
    result= db.query(SignalModel).order_by(SignalModel.id.desc()).limit(limit)
    return result

@router.post("/llm-predict", response_model=SignalOutputSchema)
async def signal_predict(data: SignalInputSchema, db: Session= Depends(get_db)):
    signal= get_signal_with_llm(data.gold_price, data.coin_price)
    
    new_signal= SignalModel(
        gold_price= data.gold_price,
        coin_price= data.coin_price,
        signal= signal
    )
    
    db.add(new_signal)
    db.commit()
    db.refresh(new_signal)

    return new_signal
    