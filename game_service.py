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

        # Baron-Fähigkeit anwenden: Wenn Baron im Spiel ist, ersetze 2 Townsfolk durch Outsider
        characters = self._apply_baron_ability(game, characters)

        random.shuffle(characters)

        # Charaktere an Spieler verteilen (nicht an Erzähler)
        for player, character in zip(non_storyteller_players, characters):
            player.character = character

        # Drunk-Mechanik: Drunk-Spieler erhalten eine falsche Townsfolk-Rolle
        self._assign_drunk_perceived_roles(game)

        game.started = True
        game.player_count = player_count

        return game

    def _assign_drunk_perceived_roles(self, game: Game) -> None:
        """
        Weist Drunk-Spielern eine zufällige Townsfolk-Rolle zu, die sie glauben zu sein.

        Args:
            game: Das aktuelle Spiel
        """
        # Hole alle verfügbaren Townsfolk aus der Edition
        townsfolk_characters = self.editions_data[game.edition]["characters"]["townsfolk"]

        # Finde alle Drunk-Spieler
        for player in game.players:
            if player.character and player.character.id == "drunk":
                # Wähle zufällige Townsfolk-Rolle
                fake_townsfolk_data = random.choice(townsfolk_characters)

                # Erstelle Character-Objekt für die falsche Rolle
                fake_character = Character(
                    id=fake_townsfolk_data["id"],
                    name=fake_townsfolk_data["name"],
                    ability=fake_townsfolk_data["ability"],
                    first_night=fake_townsfolk_data["first_night"],
                    other_nights=fake_townsfolk_data["other_nights"],
                    type="townsfolk"
                )

                # Weise die falsche Rolle zu
                player.perceived_character = fake_character

    def _apply_baron_ability(self, game: Game, characters: list[Character]) -> list[Character]:
        """
        Wendet die Baron-Fähigkeit an: Wenn Baron im Spiel ist, werden 2 Townsfolk durch Outsider ersetzt.

        Baron-Fähigkeit: "Es gibt 2 zusätzliche Outsider im Spiel."

        Args:
            game: Das aktuelle Spiel (wird aktualisiert, wenn Baron aktiv ist)
            characters: Liste der ausgewählten Charaktere

        Returns:
            Modifizierte Charakterliste mit ersetzten Townsfolk (falls Baron aktiv)

        Example:
            >>> chars = [washerwoman, librarian, chef, poisoner, baron, imp]
            >>> result = self._apply_baron_ability(game, chars)
            >>> # Ergebnis: 2 Townsfolk sind durch Outsider ersetzt
        """
        # Prüfe ob Baron im Spiel ist
        has_baron = any(char.id == "baron" for char in characters)

        if not has_baron:
            return characters  # Keine Änderung nötig

        print(f"🎭 Baron im Spiel erkannt! Wende Baron-Fähigkeit an...")

        # Setze Flag im Game-Objekt
        game.baron_active = True

        # Hole alle Townsfolk und Outsider aus den ausgewählten Charakteren
        townsfolk_in_game = [char for char in characters if char.type == "townsfolk"]
        other_characters = [char for char in characters if char.type != "townsfolk"]

        # Validierung: Mindestens 2 Townsfolk müssen vorhanden sein
        if len(townsfolk_in_game) < 2:
            print(f"⚠️ Warnung: Weniger als 2 Townsfolk im Spiel ({len(townsfolk_in_game)}). Baron-Fähigkeit kann nicht vollständig angewendet werden.")
            return characters

        # Hole alle verfügbaren Outsider aus der Edition
        edition_data = self.editions_data.get(game.edition, {})
        all_outsiders = edition_data.get("characters", {}).get("outsiders", [])

        # Filtere bereits im Spiel befindliche Outsider heraus
        outsiders_in_game_ids = [char.id for char in characters if char.type == "outsiders"]
        available_outsiders = [
            outsider for outsider in all_outsiders
            if outsider["id"] not in outsiders_in_game_ids
        ]

        if outsiders_in_game_ids:
            print(f"   ℹ️ Bereits vergebene Outsider: {', '.join(outsiders_in_game_ids)}")
            print(f"   ℹ️ Verfügbare Outsider für Baron: {len(available_outsiders)}")

        # Validierung: Mindestens 2 neue Outsider müssen verfügbar sein
        if len(available_outsiders) < 2:
            print(f"⚠️ Warnung: Weniger als 2 neue Outsider verfügbar ({len(available_outsiders)}). Baron-Fähigkeit kann nicht vollständig angewendet werden.")
            return characters

        # Wähle 2 zufällige Townsfolk zum Ersetzen
        townsfolk_to_replace = random.sample(townsfolk_in_game, 2)

        # Wähle 2 zufällige Outsider als Ersatz (nur aus noch nicht vergebenen)
        outsiders_to_add = random.sample(available_outsiders, 2)

        # Entferne die zu ersetzenden Townsfolk
        for townsfolk in townsfolk_to_replace:
            townsfolk_in_game.remove(townsfolk)
            print(f"   ❌ Entferne Townsfolk: {townsfolk.name}")

        # Füge die neuen Outsider hinzu
        for outsider_data in outsiders_to_add:
            outsider = Character(
                id=outsider_data["id"],
                name=outsider_data["name"],
                ability=outsider_data["ability"],
                first_night=outsider_data["first_night"],
                other_nights=outsider_data["other_nights"],
                type="outsiders"  # Wichtig: Setze den Typ explizit
            )
            townsfolk_in_game.append(outsider)
            print(f"   ✅ Füge Outsider hinzu: {outsider.name}")

        # Kombiniere alle Charaktere wieder
        result = townsfolk_in_game + other_characters

        print(f"✨ Baron-Fähigkeit erfolgreich angewendet!")

        return result

    def get_night_order(self, game_id: str) -> List[dict]:
        """Gibt die Nachtreihenfolge für den Erzähler zurück"""
        game = self.games.get(game_id)
        if not game or not game.started:
            raise ValueError("Spiel nicht gefunden oder noch nicht gestartet")

        # Sammle alle Charaktere im Spiel
        # Für Drunk: Verwende perceived_character statt character
        characters_in_game = []
        for p in game.players:
            if p.character is None:
                continue
            # Wenn Drunk: Verwende falsche Rolle für Nachtreihenfolge
            display_char = p.perceived_character if p.perceived_character else p.character
            characters_in_game.append(display_char)

        # Erste Nacht - erstelle Liste mit Infos am Anfang
        first_night_actions = []

        # Füge Minion Info und Dämon Info hinzu, wenn 7+ Spieler (ohne Storyteller)
        player_count = game.player_count or 0

        if player_count >= 7:
            # Minion Info kommt zuerst (vor allen Charakterfähigkeiten)
            first_night_actions.append({
                "name": "👿 Minion Info",
                "ability": "Zeige den Minions, wer ihr Dämon ist.",
                "order": 0.1
            })

            # Dämon Info kommt als zweites
            first_night_actions.append({
                "name": "😈 Dämon Info",
                "ability": "Zeige dem Dämon, wer seine Minions sind. Außerdem zeige ihm 3 \
                gute Charaktäre, die nicht im Spiel sind.",
                "order": 0.2
            })

        # Füge alle Charakterfähigkeiten hinzu
        first_night = sorted(
            [c for c in characters_in_game if c.first_night > 0],
            key=lambda x: x.first_night
        )

        for c in first_night:
            first_night_actions.append({
                "name": c.name,
                "ability": c.ability,
                "order": c.first_night
            })

        # Sortiere nach Reihenfolge
        first_night_actions.sort(key=lambda x: x["order"])

        # Andere Nächte
        other_nights = sorted(
            [c for c in characters_in_game if c.other_nights > 0],
            key=lambda x: x.other_nights
        )

        return {
            "first_night": first_night_actions,
            "other_nights": [
                {"name": c.name, "ability": c.ability, "order": c.other_nights}
                for c in other_nights
            ]
        }

    def get_player_role(self, game_id: str, player_id: str) -> Optional[Character]:
        """
        Gibt die Rolle eines Spielers zurück.

        Für Drunk-Spieler: Gibt die falsche Townsfolk-Rolle zurück (perceived_character).
        Für alle anderen: Gibt die echte Rolle zurück (character).
        """
        game = self.games.get(game_id)
        if not game:
            return None

        for player in game.players:
            if player.id == player_id:
                # Wenn Drunk: Gib die falsche Rolle zurück
                if player.perceived_character:
                    return player.perceived_character
                # Ansonsten: Gib echte Rolle zurück
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
        players_overview = []
        for p in game.players:
            if p.is_storyteller:
                continue

            # Für Drunk: Zeige perceived_character statt character
            display_character = p.perceived_character if p.perceived_character else p.character

            player_data = {
                "name": p.name,
                "player_id": p.id,  # Wichtig für Flag-Operationen
                "character": display_character.name if display_character else None,
                "character_id": display_character.id if display_character else None,  # Für Bildpfade
                "ability": display_character.ability if display_character else None,
                "type": display_character.type if display_character else None,
                "is_drunk": bool(p.perceived_character),  # True wenn Drunk
                "flags": p.flags,  # Aktive Flags
                "flag_metadata": p.flag_metadata  # Metadata zu Flags
            }

            players_overview.append(player_data)

        night_order = self.get_night_order(game_id) if game.started else None

        return {
            "game_id": game.id,
            "edition": game.edition,
            "started": game.started,
            "players": players_overview,
            "night_order": night_order,
            "baron_active": game.baron_active  # Info ob Baron-Fähigkeit aktiv ist
        }

    def set_player_flag(
        self,
        game_id: str,
        player_id: str,
        flag_type: str,
        storyteller_id: str,
        metadata: Optional[Dict] = None
    ) -> Player:
        """
        Setzt ein Flag für einen Spieler.

        Args:
            game_id: Spiel-ID
            player_id: Spieler-ID
            flag_type: Typ des Flags (z.B. "poisoned", "demon")
            storyteller_id: ID des Erzählers (zur Validierung)
            metadata: Optional - Zusätzliche Informationen zum Flag

        Returns:
            Aktualisierter Player

        Raises:
            ValueError: Wenn Spiel/Spieler nicht existiert oder Berechtigung fehlt

        Example:
            >>> player = service.set_player_flag("abc123", "player1", "poisoned", "storyteller1")
            >>> assert "poisoned" in player.flags
            >>> assert player.flags["poisoned"] == True
        """
        game = self.games.get(game_id)
        if not game:
            raise ValueError(f"Spiel {game_id} nicht gefunden")

        # Validiere Storyteller-Berechtigung
        storyteller = next(
            (p for p in game.players if p.id == storyteller_id and p.is_storyteller),
            None
        )
        if not storyteller:
            raise ValueError("Nur der Erzähler kann Flags setzen")

        # Finde Spieler
        player = next((p for p in game.players if p.id == player_id), None)
        if not player:
            raise ValueError(f"Spieler {player_id} nicht gefunden")

        if player.is_storyteller:
            raise ValueError("Erzähler können keine Flags erhalten")

        # Setze Flag
        player.flags[flag_type] = True

        # Setze Metadata wenn vorhanden
        if metadata:
            player.flag_metadata[flag_type] = metadata

        return player

    def remove_player_flag(
        self,
        game_id: str,
        player_id: str,
        flag_type: str,
        storyteller_id: str
    ) -> Player:
        """
        Entfernt ein Flag von einem Spieler.

        Args:
            game_id: Spiel-ID
            player_id: Spieler-ID
            flag_type: Typ des Flags (z.B. "poisoned")
            storyteller_id: ID des Erzählers (zur Validierung)

        Returns:
            Aktualisierter Player

        Raises:
            ValueError: Wenn Spiel/Spieler nicht existiert oder Berechtigung fehlt

        Example:
            >>> player = service.remove_player_flag("abc123", "player1", "poisoned", "storyteller1")
            >>> assert "poisoned" not in player.flags or player.flags["poisoned"] == False
        """
        game = self.games.get(game_id)
        if not game:
            raise ValueError(f"Spiel {game_id} nicht gefunden")

        # Validiere Storyteller-Berechtigung
        storyteller = next(
            (p for p in game.players if p.id == storyteller_id and p.is_storyteller),
            None
        )
        if not storyteller:
            raise ValueError("Nur der Erzähler kann Flags entfernen")

        # Finde Spieler
        player = next((p for p in game.players if p.id == player_id), None)
        if not player:
            raise ValueError(f"Spieler {player_id} nicht gefunden")

        # Entferne Flag
        if flag_type in player.flags:
            del player.flags[flag_type]

        # Entferne Metadata
        if flag_type in player.flag_metadata:
            del player.flag_metadata[flag_type]

        return player

    def get_player_flags(self, game_id: str, player_id: str) -> Dict[str, bool]:
        """
        Gibt alle aktiven Flags eines Spielers zurück.

        Args:
            game_id: Spiel-ID
            player_id: Spieler-ID

        Returns:
            Dictionary mit aktiven Flags

        Raises:
            ValueError: Wenn Spiel/Spieler nicht existiert
        """
        game = self.games.get(game_id)
        if not game:
            raise ValueError(f"Spiel {game_id} nicht gefunden")

        player = next((p for p in game.players if p.id == player_id), None)
        if not player:
            raise ValueError(f"Spieler {player_id} nicht gefunden")

        return player.flags

    def clear_temporary_flags(self, game_id: str, storyteller_id: str) -> Game:
        """
        Entfernt alle temporären Flags (z.B. "poisoned" nach einer Nacht).

        Args:
            game_id: Spiel-ID
            storyteller_id: ID des Erzählers (zur Validierung)

        Returns:
            Aktualisiertes Game-Objekt

        Raises:
            ValueError: Wenn Spiel nicht existiert oder Berechtigung fehlt

        Example:
            >>> game = service.clear_temporary_flags("abc123", "storyteller1")
            >>> # Alle "poisoned" Flags wurden entfernt
        """
        game = self.games.get(game_id)
        if not game:
            raise ValueError(f"Spiel {game_id} nicht gefunden")

        # Validiere Storyteller-Berechtigung
        storyteller = next(
            (p for p in game.players if p.id == storyteller_id and p.is_storyteller),
            None
        )
        if not storyteller:
            raise ValueError("Nur der Erzähler kann Flags löschen")

        # Definiere temporäre Flags (erweitern nach Bedarf)
        TEMPORARY_FLAGS = {"poisoned", "protected", "used_ability"}

        # Entferne temporäre Flags von allen Spielern
        for player in game.players:
            if not player.is_storyteller:
                for flag in TEMPORARY_FLAGS:
                    if flag in player.flags:
                        del player.flags[flag]
                    if flag in player.flag_metadata:
                        del player.flag_metadata[flag]

        return game


# Singleton-Instanz
game_service = GameService()


