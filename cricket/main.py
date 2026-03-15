from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

app = FastAPI()

# Database Simulation
tournaments = []
teams = []
players = []

# Tournament Model
class Tournament(BaseModel):
    banner: str
    logo: str
    tournament_name: str
    organizer_name: str
    city: str
    phone_number: str
    email: EmailStr
    start_date: date
    end_date: date
    need_more_teams: bool


# Team Model
class Team(BaseModel):
    id: int
    tournament_id: int
    name: str
    captain_email: EmailStr
    admin_email: EmailStr
    entry_fees: float
    winning_prize: str  # cash, trophy, both

# Player Model
class Player(BaseModel):
    id: int
    team_id: int
    name: str
    email: EmailStr
    role: str  # Player, Vice-Captain, etc.

# Endpoint: Create Tournament (Organizer only)
# Create Tournament
@app.post("/create_tournament/")
async def create_tournament(tournament: Tournament):
    tournament_id = len(tournaments) + 1
    tournament_data = {"id": tournament_id, **tournament.dict()}
    tournaments.append(tournament_data)
    return {"message": "Tournament created successfully!", "tournament_id": tournament_id}


# Endpoint: Create Team (Organizer only)
@app.post("/create_team/")
async def create_team(team: Team):
    # Check if tournament exists
    if not any(t["id"] == team.tournament_id for t in tournaments):
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    teams.append(team.dict())
    return {"message": "Team created successfully!", "team_id": team.id}

# Endpoint: Add Player (Only Captain/Admin can add)
@app.post("/add_player/")
async def add_player(player: Player):
    # Check if team exists
    team = next((t for t in teams if t["id"] == player.team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if email matches the captain or admin
    if player.email in (team["captain_email"], team["admin_email"]):
        raise HTTPException(status_code=400, detail="Captain/Admin cannot be a player")

    players.append(player.dict())
    return {"message": "Player added successfully!", "player_id": player.id}

# Endpoint: Edit Team Details (Only Captain/Admin can edit)
@app.put("/edit_team/{team_id}/")
async def edit_team(team_id: int, updated_team: Team):
    for i, team in enumerate(teams):
        if team["id"] == team_id:
            teams[i].update(updated_team.dict())
            return {"message": "Team details updated successfully!"}
    
    raise HTTPException(status_code=404, detail="Team not found")

# Endpoint: Get All Teams
@app.get("/teams/")
async def get_teams():
    return teams

# Endpoint: Get All Players
@app.get("/players/")
async def get_players():
    return players

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
