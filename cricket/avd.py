from pprint import pprint

def create_tournment(teams, type="group+knockout", no_groups=2):
    if type != "group+knockout":
        exit(1)

    groups = []
    for i in range(no_groups):
        group = []
        for j in range(i, len(teams), no_groups):
            group.append(teams[j])
        groups.append(group)
    print("groups: ", groups)    
    
    matches = []
    for group in groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                matches.append((group[i], group[j]))
    
    print("matches: ", matches)

    return {
        "groups": groups,
        "matches": matches
    }

def play_match(batting_team, fielding_team, overs=5):
    print(f"playing match between {batting_team} and {fielding_team}")
    
    # 1st innings
    batting_team_runs, batting_team_wickets = 0, 0
    print(f"Innings 1: Batting team is {batting_team}")
    for over in range(overs):
        runs = int(input(f"Runs for over {over+1} / team {batting_team}: "))
        wickets = int(input(f"Wickets for over {over+1} / team {batting_team}: "))
        batting_team_runs += runs
        batting_team_wickets += wickets
        if batting_team_wickets >= 10:
            break

    print(f"\n\n# Innings 1 {batting_team}: {batting_team_runs}/{batting_team_wickets}")    
    target = batting_team_runs + 1
    
    # 2nd innings
    fielding_team_runs, fielding_team_wickets = 0, 0
    print(f"Innings 2: Batting team is {fielding_team}")
    for over in range(overs):
        runs = int(input(f"Runs for over {over+1} / team {fielding_team}: "))
        wickets = int(input(f"Wickets for over {over+1} / team {fielding_team}: "))
        fielding_team_runs += runs
        fielding_team_wickets += wickets
        
        # Check if second team has won or lost
        if fielding_team_runs >= target:
            print(f"{fielding_team} has chased the target and won the match!")
            winner = fielding_team
            break
        elif fielding_team_wickets >= 10:
            print(f"{batting_team} wins as {fielding_team} lost all wickets!")
            winner = batting_team
            break
    else:
        winner = batting_team if fielding_team_runs < batting_team_runs else fielding_team
    
    print(f"Winner: {winner}")
    
    return {
        "batting_team": batting_team,
        "fielding_team": fielding_team,
        "batting_team_runs": batting_team_runs,
        "batting_team_wickets": batting_team_wickets,
        "fielding_team_runs": fielding_team_runs,
        "fielding_team_wickets": fielding_team_wickets,
        "winner": winner
    }

t1 = create_tournment(['a','b','c','d','e', 'f'])    
m1 = play_match(t1['matches'][0][0], t1['matches'][0][1], 5)

pprint(m1)
