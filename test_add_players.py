#!/usr/bin/env python3
"""
Test-Script zum automatischen Hinzufügen von Spielern zu einem Spiel.

Verwendung:
    python test_add_players.py --game <game_id> --count 6
    python test_add_players.py --game abc123 --count 10 --start
"""

import argparse
import requests
import sys
from typing import Optional


class GameTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def create_game(self, edition: str = "TroubleBrewing", storyteller_name: str = "TestStoryteller") -> dict:
        """Erstellt ein neues Spiel und gibt game_id und storyteller_id zurück."""
        print(f"📝 Erstelle neues Spiel...")

        response = self.session.post(
            f"{self.base_url}/api/game/create",
            json={
                "edition": edition,
                "storyteller_name": storyteller_name
            }
        )

        if response.status_code != 200:
            print(f"❌ Fehler beim Erstellen des Spiels: {response.status_code}")
            print(response.text)
            sys.exit(1)

        data = response.json()
        print(f"✅ Spiel erstellt!")
        print(f"   Game ID: {data['game_id']}")
        print(f"   Storyteller ID: {data['storyteller_id']}")
        print(f"   Join URL: {self.base_url}{data['join_url']}")

        return data

    def add_player(self, game_id: str, player_name: str) -> dict:
        """Fügt einen Spieler zu einem Spiel hinzu."""
        response = self.session.post(
            f"{self.base_url}/api/game/{game_id}/join",
            json={"player_name": player_name}
        )

        if response.status_code != 200:
            print(f"❌ Fehler beim Hinzufügen von {player_name}: {response.status_code}")
            print(response.text)
            return None

        return response.json()

    def add_players(self, game_id: str, count: int, name_prefix: str = "Player") -> list:
        """Fügt mehrere Spieler zu einem Spiel hinzu."""
        print(f"\n👥 Füge {count} Spieler hinzu...")

        players = []
        for i in range(1, count + 1):
            player_name = f"{name_prefix}{i}"
            player_data = self.add_player(game_id, player_name)

            if player_data:
                players.append(player_data)
                print(f"   ✅ {player_name} hinzugefügt (ID: {player_data['player_id']})")
            else:
                print(f"   ❌ {player_name} konnte nicht hinzugefügt werden")

        print(f"\n✅ {len(players)} von {count} Spielern erfolgreich hinzugefügt!")
        return players

    def start_game(self, game_id: str, player_count: int) -> bool:
        """Startet das Spiel mit der angegebenen Spielerzahl."""
        print(f"\n🎮 Starte Spiel mit {player_count} Spielern...")

        response = self.session.post(
            f"{self.base_url}/api/game/{game_id}/start",
            json={"player_count": player_count}
        )

        if response.status_code != 200:
            print(f"❌ Fehler beim Starten des Spiels: {response.status_code}")
            print(response.text)
            return False

        print(f"✅ Spiel gestartet! Rollen wurden verteilt!")
        return True

    def get_game_overview(self, game_id: str, storyteller_id: str) -> dict:
        """Holt die Spielübersicht vom Server."""
        response = self.session.get(
            f"{self.base_url}/api/storyteller/{game_id}/{storyteller_id}/overview"
        )

        if response.status_code != 200:
            print(f"❌ Fehler beim Abrufen der Übersicht: {response.status_code}")
            return None

        return response.json()

    def show_player_roles(self, game_id: str, storyteller_id: str, player_ids: dict = None):
        """Zeigt die verteilten Rollen an."""
        overview = self.get_game_overview(game_id, storyteller_id)

        if not overview:
            return

        print("\n" + "="*60)
        print("🎭 SPIELÜBERSICHT")
        print("="*60)
        print(f"Spiel-ID: {overview['game_id']}")
        print(f"Edition: {overview['edition']}")
        print(f"Status: {'✅ Gestartet' if overview['started'] else '⏳ Warte auf Start'}")
        print(f"\n👥 Spieler ({len(overview['players'])}):")
        print("-"*60)

        for player in overview['players']:
            if player['character']:
                drunk_badge = " 🥴 DRUNK" if player.get('is_drunk') else ""
                role_info = f"{player['character']:20} ({player['type']:10}){drunk_badge}"

                # Zeige Spieler-Link wenn player_ids vorhanden
                player_link = ""
                if player_ids and player['name'] in player_ids:
                    pid = player_ids[player['name']]
                    player_link = f"\n      🔗 {self.base_url}/player.html?game={game_id}&player={pid}"

                print(f"  {player['name']:15} | {role_info}{player_link}")
            else:
                print(f"  {player['name']:15} | (Keine Rolle zugewiesen)")

        if overview.get('night_order'):
            print(f"\n🌙 Nachtreihenfolge - Erste Nacht:")
            print("-"*60)
            for item in overview['night_order']['first_night']:
                print(f"  {item['order']:5.1f} | {item['name']}")

        print("="*60)

    def quick_test(self, player_count: int, edition: str = "TroubleBrewing", auto_start: bool = True):
        """Kompletter Quick-Test: Spiel erstellen, Spieler hinzufügen, optional starten."""
        print("\n" + "="*60)
        print("🚀 QUICK TEST MODE")
        print("="*60)

        # Spiel erstellen
        game_data = self.create_game(edition=edition)
        game_id = game_data['game_id']
        storyteller_id = game_data['storyteller_id']

        # Spieler hinzufügen
        players = self.add_players(game_id, player_count)

        # Erstelle Mapping: Spielername -> Player ID
        player_ids = {f"Player{i+1}": player['player_id'] for i, player in enumerate(players)}

        # Optional: Spiel starten
        if auto_start:
            self.start_game(game_id, player_count)
            self.show_player_roles(game_id, storyteller_id, player_ids)

        print("\n" + "="*60)
        print("📋 STORYTELLER LINKS:")
        print("="*60)
        print(f"🎭 Storyteller-Ansicht: {self.base_url}/storyteller.html?game={game_id}&storyteller={storyteller_id}")
        print(f"👥 Spieler-Join-URL: {self.base_url}/join.html?game={game_id}")
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Test-Script für Blood on the Clocktower - Automatisches Spieler-Hinzufügen"
    )

    # Haupt-Modi
    parser.add_argument(
        '--quick', '-q',
        type=int,
        metavar='COUNT',
        help='Quick Mode: Erstellt neues Spiel mit COUNT Spielern und startet es'
    )

    # Manueller Modus
    parser.add_argument(
        '--game', '-g',
        type=str,
        help='Game ID (für manuellen Modus)'
    )

    parser.add_argument(
        '--count', '-c',
        type=int,
        default=5,
        help='Anzahl der Spieler (Standard: 5)'
    )

    parser.add_argument(
        '--start', '-s',
        action='store_true',
        help='Spiel nach Hinzufügen der Spieler automatisch starten'
    )

    parser.add_argument(
        '--edition', '-e',
        type=str,
        default='TroubleBrewing',
        choices=['TroubleBrewing', 'SectsAndViolets'],
        help='Edition (Standard: TroubleBrewing)'
    )

    parser.add_argument(
        '--url',
        type=str,
        default='http://localhost:8000',
        help='Server URL (Standard: http://localhost:8000)'
    )

    parser.add_argument(
        '--prefix',
        type=str,
        default='Player',
        help='Präfix für Spielernamen (Standard: Player)'
    )

    args = parser.parse_args()

    # Initialisiere Tester
    tester = GameTester(base_url=args.url)

    # Quick Mode
    if args.quick:
        tester.quick_test(
            player_count=args.quick,
            edition=args.edition,
            auto_start=True
        )
        return

    # Manueller Modus
    if args.game:
        # Spieler zu bestehendem Spiel hinzufügen
        tester.add_players(args.game, args.count, args.prefix)

        if args.start:
            tester.start_game(args.game, args.count)
            # Storyteller ID nicht bekannt im manuellen Modus
            print("\n💡 Tipp: Öffne die Storyteller-Ansicht im Browser um die Rollen zu sehen!")
    else:
        # Kein Modus gewählt - zeige Hilfe
        parser.print_help()
        print("\n" + "="*60)
        print("📚 BEISPIELE:")
        print("="*60)
        print("# Quick Test mit 6 Spielern:")
        print("  python test_add_players.py --quick 6")
        print()
        print("# Quick Test mit 10 Spielern (Trouble Brewing):")
        print("  python test_add_players.py -q 10")
        print()
        print("# Quick Test mit 7 Spielern (Sects & Violets):")
        print("  python test_add_players.py -q 7 -e SectsAndViolets")
        print()
        print("# Zu bestehendem Spiel 5 Spieler hinzufügen:")
        print("  python test_add_players.py --game abc123 --count 5")
        print()
        print("# Zu bestehendem Spiel 7 Spieler hinzufügen und starten:")
        print("  python test_add_players.py -g abc123 -c 7 --start")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()

