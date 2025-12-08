from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from models import CreateGameRequest, JoinGameRequest, StartGameRequest
from game_service import game_service
import uvicorn

app = FastAPI(title="Blood on the Clocktower")

# API Endpoints

@app.get("/api/editions")
async def get_editions():
    """Gibt alle verfügbaren Editionen zurück"""
    return game_service.get_editions()


@app.get("/api/editions/{edition}/characters")
async def get_edition_characters(edition: str):
    """Gibt alle Charaktere einer Edition zurück"""
    try:
        return game_service.get_edition_characters(edition)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    """Erstellt ein neues Spiel"""
    try:
        game = game_service.create_game(request.edition, request.storyteller_name)
        storyteller = next(p for p in game.players if p.is_storyteller)
        return {
            "game_id": game.id,
            "edition": game.edition,
            "storyteller_id": storyteller.id,
            "join_url": f"/join.html?game={game.id}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/game/{game_id}")
async def get_game(game_id: str):
    """Gibt Informationen über ein Spiel zurück"""
    game = game_service.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Spiel nicht gefunden")

    return {
        "id": game.id,
        "edition": game.edition,
        "started": game.started,
        "player_count": len([p for p in game.players if not p.is_storyteller])
    }


@app.post("/api/game/{game_id}/join")
async def join_game(game_id: str, request: JoinGameRequest):
    """Spieler tritt einem Spiel bei"""
    try:
        player = game_service.join_game(game_id, request.player_name)
        return {
            "player_id": player.id,
            "name": player.name,
            "game_id": game_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/game/{game_id}/start")
async def start_game(game_id: str, request: StartGameRequest):
    """Startet das Spiel und verteilt Rollen"""
    try:
        game = game_service.start_game(game_id, request.player_count)
        return {
            "game_id": game.id,
            "started": True,
            "message": "Spiel gestartet! Rollen wurden verteilt."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/player/{game_id}/{player_id}/role")
async def get_player_role(game_id: str, player_id: str):
    """Gibt die Rolle eines Spielers zurück"""
    character = game_service.get_player_role(game_id, player_id)
    if not character:
        raise HTTPException(status_code=404, detail="Rolle nicht gefunden")

    return {
        "name": character.name,
        "ability": character.ability,
        "type": character.type
    }


@app.get("/api/storyteller/{game_id}/{storyteller_id}/overview")
async def get_storyteller_overview(game_id: str, storyteller_id: str):
    """Gibt die Erzähler-Übersicht zurück"""
    try:
        return game_service.get_storyteller_overview(game_id, storyteller_id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Hauptseite - Edition auswählen"""
    return FileResponse("static/index.html")


@app.get("/join.html", response_class=HTMLResponse)
async def join_page():
    """Beitritts-Seite"""
    return FileResponse("static/join.html")


@app.get("/player.html", response_class=HTMLResponse)
async def player_page():
    """Spieler-Ansicht"""
    return FileResponse("static/player.html")


@app.get("/storyteller.html", response_class=HTMLResponse)
async def storyteller_page():
    """Erzähler-Ansicht"""
    return FileResponse("static/storyteller.html")


# Statische Dateien
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    print("🎭 Blood on the Clocktower Server gestartet!")
    print("📱 Öffne http://localhost:8000 im Browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
