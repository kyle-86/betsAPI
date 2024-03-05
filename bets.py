from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend on localhost
origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the port of your frontend if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close

class Bet(BaseModel):
  
  refrenceId : str = None

  teams : str = None
  sport : str = None
  league : str = None
  eventTime : str = None

  agency : str = None
  line : str = None
  value : str = None
  betType : str = None
  betTeam : str = None
  betAmount : str = None
  odds : str = None

  betResult : str = None

BETS = []

@app.get("/")
def read_api(db: Session = Depends(get_db)):
  return db.query(models.Bets).all()

@app.post("/")
async def create_bet(bet: Bet, db: Session = Depends(get_db)):
  
  bet_model = models.Bets()
  bet_model.refrenceId = bet.refrenceId
  bet_model.teams = bet.teams
  bet_model.sport = bet.sport
  bet_model.league = bet.league
  bet_model.eventTime = bet.eventTime
  bet_model.agency = bet.agency
  bet_model.line = bet.line
  bet_model.value = bet.value
  bet_model.betType = bet.betType
  bet_model.betTeam = bet.betTeam
  bet_model.odds = bet.odds
  bet_model.betResult = bet.betResult

  db.add(bet_model)
  db.commit()

  return bet

@app.put("/{bet_id}")
def update_bet(bet_id: int, bet: Bet, db: Session = Depends(get_db)):
  
  bet_model = db.query(models.Bets).filter(models.Bets.id == bet_id).first()
  

  if bet_model is None:
    raise HTTPException(
      status_code=404,
      detail=f"ID {bet_id} : Does not exist"
    )
  
  bet_model.refrenceId = bet.refrenceId
  bet_model.teams = bet.teams
  bet_model.sport = bet.sport
  bet_model.league = bet.league
  bet_model.eventTime = bet.eventTime
  bet_model.agency = bet.agency
  bet_model.line = bet.line
  bet_model.value = bet.value
  bet_model.betType = bet.betType
  bet_model.betTeam = bet.betTeam
  bet_model.odds = bet.odds
  bet_model.betResult = bet.betResult

  db.add(bet_model)
  db.commit()

  return bet

@app.delete("/{bet_id}")
def delete_bet(bet_id: int, db: Session = Depends(get_db)):

  bet_model = db.query(models.Bets).filter(models.Bets.id == bet_id).first()

  if bet_model is None:
    raise HTTPException(
      status_code=404,
      detail=f"ID {bet_id} : Does not exist"
    )

  db.query(models.Bets).filter(models.Bets.id == bet_id).delete()
  db.commit()