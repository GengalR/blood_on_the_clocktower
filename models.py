from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum


class Team(str, Enum):
    GOOD = "good"
    EVIL = "evil"


class CharacterType(str, Enum):
    TOWNSFOLK = "townsfolk"
    OUTSIDER = "outsiders"
    MINION = "minions"
    DEMON = "demons"


class FlagType(str, Enum):
    """Spielmechanische Flags für Spieler-Status"""
    POISONED = "poisoned"  # 🧪 Vergiftet (Poisoner-Fähigkeit)
    DEMON = "demon"  # 👹 Dämon-Markierung
    RED_HERRING = "red_herring"  # 🎯 Red Herring (Fortune Teller)
    DEAD = "dead"  # 💀 Tot
    USED_ABILITY = "used_ability"  # ✅ Fähigkeit bereits genutzt
    PROTECTED = "protected"  # 🛡️ Geschützt (Monk-Fähigkeit)
    MASTER = "master"  # 🎓 Meister
    # Weitere Flags können hier ergänzt werden


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
    perceived_character: Optional[Character] = None  # Für Drunk: Die Rolle, die der Spieler glaubt zu sein
    is_storyteller: bool = False
    flags: Dict[str, bool] = {}  # Aktive Flags (z.B. {"poisoned": True, "demon": True})
    flag_metadata: Dict[str, Any] = {}  # Zusätzliche Flag-Infos (z.B. Zeitstempel, Dauer)


class Game(BaseModel):
    id: str
    edition: str
    players: List[Player] = []
    started: bool = False
    player_count: Optional[int] = None
    baron_active: bool = False  # True wenn Baron-Fähigkeit angewendet wurde


class CreateGameRequest(BaseModel):
    edition: str
    storyteller_name: str


class JoinGameRequest(BaseModel):
    player_name: str


class StartGameRequest(BaseModel):
    player_count: int


class SetPlayerFlagRequest(BaseModel):
    """Request zum Setzen eines Player-Flags"""
    flag_type: FlagType
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flag_type": "poisoned",
                "metadata": {
                    "set_by": "storyteller_id",
                    "night": 1,
                    "expires_after_night": True
                }
            }
        }
    )


class RemovePlayerFlagRequest(BaseModel):
    """Request zum Entfernen eines Player-Flags"""
    flag_type: FlagType

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flag_type": "poisoned"
            }
        }
    )


