import requests

# Define API URL
BASE_URL = "http://localhost:5000/api"  # Replace with the actual API base URL

# Define tournament
tournament = {
    "name": "BITPL 2025",
    "start_date": "2025-03-10",
    "end_date": "2025-03-20",
    "description": "LETS PLAY BIT",
    "logo_url": "https://example.com/ipl-logo.png",
    "status": "upcoming"
}

# Define teams
teams = [
    {"name": "INDIA", "logo_url": "https://logo.com/india.png"},
    {"name": "AUSTRALIA", "logo_url": "https://logo.com/australia.png"},
    {"name": "ENGLAND", "logo_url": "https://logo.com/england.png"},
    {"name": "SOUTH AFRICA", "logo_url": "https://logo.com/southafrica.png"},
    {"name": "NEW ZEALAND", "logo_url": "https://logo.com/newzealand.png"}
]

# Define players for each team
players = {
    "INDIA": [
        {"name": "Rohit Sharma", "jersey_number": 45, "role": "batsman"},
        {"name": "Virat Kohli", "jersey_number": 18, "role": "batsman"},
        {"name": "Shubman Gill", "jersey_number": 77, "role": "batsman"},
        {"name": "Suryakumar Yadav", "jersey_number": 63, "role": "batsman"},
        {"name": "Hardik Pandya", "jersey_number": 33, "role": "all-rounder"},
        {"name": "Ravindra Jadeja", "jersey_number": 8, "role": "all-rounder"},
        {"name": "Rishabh Pant", "jersey_number": 17, "role": "wicketkeeper"},
        {"name": "Jasprit Bumrah", "jersey_number": 93, "role": "bowler"},
        {"name": "Mohammed Shami", "jersey_number": 11, "role": "bowler"},
        {"name": "Kuldeep Yadav", "jersey_number": 23, "role": "bowler"},
        {"name": "Yuzvendra Chahal", "jersey_number": 3, "role": "bowler"}
    ],
    "AUSTRALIA": [
        {"name": "David Warner", "jersey_number": 31, "role": "batsman"},
        {"name": "Steve Smith", "jersey_number": 49, "role": "batsman"},
        {"name": "Marnus Labuschagne", "jersey_number": 33, "role": "batsman"},
        {"name": "Glenn Maxwell", "jersey_number": 32, "role": "all-rounder"},
        {"name": "Marcus Stoinis", "jersey_number": 15, "role": "all-rounder"},
        {"name": "Alex Carey", "jersey_number": 4, "role": "wicketkeeper"},
        {"name": "Pat Cummins", "jersey_number": 30, "role": "bowler"},
        {"name": "Mitchell Starc", "jersey_number": 56, "role": "bowler"},
        {"name": "Josh Hazlewood", "jersey_number": 38, "role": "bowler"},
        {"name": "Adam Zampa", "jersey_number": 88, "role": "bowler"},
        {"name": "Nathan Lyon", "jersey_number": 67, "role": "bowler"}
    ],
    "ENGLAND": [
        {"name": "Joe Root", "jersey_number": 66, "role": "batsman"},
        {"name": "Ben Stokes", "jersey_number": 55, "role": "all-rounder"},
        {"name": "Jos Buttler", "jersey_number": 63, "role": "wicketkeeper"},
        {"name": "Jofra Archer", "jersey_number": 22, "role": "bowler"},
        {"name": "Chris Woakes", "jersey_number": 19, "role": "all-rounder"}
    ] * 2,
    "SOUTH AFRICA": [
        {"name": "Quinton de Kock", "jersey_number": 12, "role": "wicketkeeper"},
        {"name": "Kagiso Rabada", "jersey_number": 25, "role": "bowler"},
        {"name": "David Miller", "jersey_number": 10, "role": "batsman"}
    ] * 4,
    "NEW ZEALAND": [
        {"name": "Kane Williamson", "jersey_number": 22, "role": "batsman"},
        {"name": "Trent Boult", "jersey_number": 18, "role": "bowler"}
    ] * 6
}

# Function to create tournament
def create_tournament(tournament):
    response = requests.post(f"{BASE_URL}/tournaments", json=tournament)
    return response.json()[0].get("id") if response.status_code == 200 else exit(1)

# Function to create team
def create_team(team):
    response = requests.post(f"{BASE_URL}/teams", json=team)
    return response.json()[0].get("id") if response.status_code == 200 else exit(1)

# Function to create player
def create_player(player, team_id):
    player["team_id"] = team_id
    requests.post(f"{BASE_URL}/players", json=player)

# Create tournament
tournament_id = create_tournament(tournament)

# Create teams and add players
team_ids = {team["name"]: create_team(team) for team in teams}
for team_name, team_id in team_ids.items():
    for player in players.get(team_name, [])[:11]:
        create_player(player, team_id)

print("Tournament, teams, and players created successfully!")
