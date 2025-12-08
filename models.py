from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum


class Team(str, Enum):
    GOOD = "good"
    EVIL = "evil"


class CharacterType(str, Enum):
    TOWNSFOLK = "townsfolk"
    OUTSIDER = "outsiders"
    MINION = "minions"
    DEMON = "demons"


class Character(BaseModel):
    id: str
    name: str
    ability: str
    first_night: int
    other_nights: int
    type: Optional[CharacterType] = None


class Player(BaseModel):
    id: str
    name: str
    character: Optional[Character] = None
    is_storyteller: bool = False


class Game(BaseModel):
    id: str
    edition: str
    players: List[Player] = []
    started: bool = False
    player_count: Optional[int] = None


class CreateGameRequest(BaseModel):
    edition: str
    storyteller_name: str


class JoinGameRequest(BaseModel):
    player_name: str


class StartGameRequest(BaseModel):
    player_count: int

