import requests

# Define API URL
BASE_URL = "http://localhost:5000/api"  # Replace with the actual API base URL

# Define teams
teams = [
    {"name": "INDIA", "logo_url": "https://logo.com/india.png"},
    {"name": "AUSTRALIA", "logo_url": "https://logo.com/australia.png"}
]

# Define players
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
    ]
}

# Function to create a team
def create_team(team):
    response = requests.post(f"{BASE_URL}/teams", json=team)
    if response.status_code == 200:
        return response.json()[0].get("id")
    else:
        print(f"Failed to create team {team['name']}: {response.text}")
        return None

# Function to create a player
def create_player(player, team_id):
    player["team_id"] = team_id
    response = requests.post(f"{BASE_URL}/players", json=player)
    if response.status_code != 200:
        print(f"Failed to create player {player['name']}: {response.text}")

# Create teams and add players
team_ids = {}
for team in teams:
    team_id = create_team(team)
    if team_id:
        team_ids[team["name"]] = team_id
        for player in players[team["name"]]:
            create_player(player, team_id)

print("Teams and players created successfully!")
