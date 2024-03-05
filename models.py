from sqlalchemy import Column, Integer, String
from database import Base

class Bets(Base):
  __tablename__ = "bets"

  id = Column(Integer, primary_key=True, index=True)
  refrenceId = Column(String)

  teams = Column(String)
  sport = Column(String)
  league = Column(String)
  eventTime = Column(String)

  agency = Column(String)
  line = Column(String)
  value = Column(String)
  betType = Column(String)
  betTeam = Column(String)
  odds = Column(String)

  betResult = Column(String)
