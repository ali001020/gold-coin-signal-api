from sqlalchemy import Column, Integer, Float, DateTime, String, func
from core.database import Base

class SignalModel(Base):
    __tablename__= "signals"
    
    id= Column(Integer, primary_key= True, autoincrement= True)
    gold_price= Column(Float, nullable= False)
    coin_price= Column(Float, nullable= False)
    signal= Column(String, nullable= False)
    
    created_at= Column(DateTime, server_default= func.now())