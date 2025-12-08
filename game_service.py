import json
import random
import uuid
from typing import Dict, List, Optional
from models import Game, Player, Character, CharacterType, Team


class GameService:
    def __init__(self):
        self.games: Dict[str, Game] = {}
        self.editions_data = self._load_editions()

    def _load_editions(self) -> dict:
        """Lade Editions-Daten aus JSON"""
        with open('data/editions.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_editions(self) -> List[dict]:
        """Gibt alle verfügbaren Editionen zurück"""
        return [
            {"id": key, "name": value["name"]}
            for key, value in self.editions_data.items()
        ]

    def get_edition_characters(self, edition: str) -> dict:
        """Gibt alle Charaktere einer Edition zurück"""
        if edition not in self.editions_data:
            raise ValueError(f"Edition {edition} nicht gefunden")

        edition_data = self.editions_data[edition]
        characters = edition_data["characters"]

        # Füge CharacterType zu jedem Charakter hinzu
        result = {}
        for char_type, char_list in characters.items():
            result[char_type] = [
                {**char, "type": char_type}
                for char in char_list
            ]

        return result

    def create_game(self, edition: str, storyteller_name: str) -> Game:
        """Erstellt ein neues Spiel"""
        if edition not in self.editions_data:
            raise ValueError(f"Edition {edition} nicht gefunden")

        game_id = str(uuid.uuid4())[:8]
        storyteller = Player(
            id=str(uuid.uuid4())[:8],
            name=storyteller_name,
            is_storyteller=True
        )

        game = Game(
            id=game_id,
            edition=edition,
            players=[storyteller]
        )

        self.games[game_id] = game
        return game

    def get_game(self, game_id: str) -> Optional[Game]:
        """Gibt ein Spiel zurück"""
        return self.games.get(game_id)

    def join_game(self, game_id: str, player_name: str) -> Player:
        """Spieler tritt einem Spiel bei"""
        game = self.games.get(game_id)
        if not game:
            raise ValueError(f"Spiel {game_id} nicht gefunden")

        if game.started:
            raise ValueError("Spiel hat bereits begonnen")

        player = Player(
            id=str(uuid.uuid4())[:8],
            name=player_name,
            is_storyteller=False
        )

        game.players.append(player)
        return player

    def _get_role_distribution(self, edition: str, player_count: int) -> dict:
        """Berechnet Rollenverteilung basierend auf Spielerzahl"""
        setup = self.editions_data[edition]["setup"]

        if str(player_count) not in setup:
            raise ValueError(f"Ungültige Spielerzahl: {player_count}")

        return setup[str(player_count)]

    def _select_random_characters(
        self,
        edition: str,
        distribution: dict
    ) -> List[Character]:
        """Wählt zufällig Charaktere basierend auf Verteilung"""
        characters_data = self.editions_data[edition]["characters"]
        selected = []

        for char_type, count in distribution.items():
            available = characters_data[char_type]
            chosen = random.sample(available, min(count, len(available)))

            for char in chosen:
                character = Character(
                    id=char["id"],
                    name=char["name"],
                    ability=char["ability"],
                    first_night=char["first_night"],
                    other_nights=char["other_nights"],
                    type=char_type
                )
                selected.append(character)

        return selected

    def start_game(self, game_id: str, player_count: int) -> Game:
        """Startet das Spiel und verteilt Rollen"""
        game = self.games.get(game_id)
        if not game:
            raise ValueError(f"Spiel {game_id} nicht gefunden")

        if game.started:
            raise ValueError("Spiel hat bereits begonnen")

        # Anzahl Nicht-Erzähler Spieler
        non_storyteller_players = [p for p in game.players if not p.is_storyteller]

        if len(non_storyteller_players) != player_count:
            raise ValueError(
                f"Spieleranzahl stimmt nicht überein. "
                f"Erwartet: {player_count}, Vorhanden: {len(non_storyteller_players)}"
            )

        # Rollenverteilung berechnen
        distribution = self._get_role_distribution(game.edition, player_count)

        # Charaktere auswählen
        characters = self._select_random_characters(game.edition, distribution)
        random.shuffle(characters)

        # Charaktere an Spieler verteilen (nicht an Erzähler)
        for player, character in zip(non_storyteller_players, characters):
            player.character = character

        game.started = True
        game.player_count = player_count

        return game

    def get_night_order(self, game_id: str) -> List[dict]:
        """Gibt die Nachtreihenfolge für den Erzähler zurück"""
        game = self.games.get(game_id)
        if not game or not game.started:
            raise ValueError("Spiel nicht gefunden oder noch nicht gestartet")

        # Sammle alle Charaktere im Spiel
        characters_in_game = [
            p.character for p in game.players
            if p.character is not None
        ]

        # Erste Nacht
        first_night = sorted(
            [c for c in characters_in_game if c.first_night > 0],
            key=lambda x: x.first_night
        )

        # Andere Nächte
        other_nights = sorted(
            [c for c in characters_in_game if c.other_nights > 0],
            key=lambda x: x.other_nights
        )

        return {
            "first_night": [
                {"name": c.name, "ability": c.ability, "order": c.first_night}
                for c in first_night
            ],
            "other_nights": [
                {"name": c.name, "ability": c.ability, "order": c.other_nights}
                for c in other_nights
            ]
        }

    def get_player_role(self, game_id: str, player_id: str) -> Optional[Character]:
        """Gibt die Rolle eines Spielers zurück"""
        game = self.games.get(game_id)
        if not game:
            return None

        for player in game.players:
            if player.id == player_id:
                return player.character

        return None

    def get_storyteller_overview(self, game_id: str, player_id: str) -> dict:
        """Gibt die Erzähler-Übersicht zurück"""
        game = self.games.get(game_id)
        if not game:
            raise ValueError("Spiel nicht gefunden")

        # Prüfe ob Spieler Erzähler ist
        storyteller = next(
            (p for p in game.players if p.id == player_id and p.is_storyteller),
            None
        )

        if not storyteller:
            raise ValueError("Nur der Erzähler kann diese Ansicht sehen")

        # Erstelle Übersicht
        players_overview = [
            {
                "name": p.name,
                "character": p.character.name if p.character else None,
                "ability": p.character.ability if p.character else None,
                "type": p.character.type if p.character else None
            }
            for p in game.players if not p.is_storyteller
        ]

        night_order = self.get_night_order(game_id) if game.started else None

        return {
            "game_id": game.id,
            "edition": game.edition,
            "started": game.started,
            "players": players_overview,
            "night_order": night_order
        }


# Singleton-Instanz
game_service = GameService()


