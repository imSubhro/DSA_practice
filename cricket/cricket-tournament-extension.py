from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# Note: This is an extension to the existing cricket-scoring-api.py file
# Add these models and routes to your existing application

# New Models
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, completed
    
    stages = db.relationship('Stage', backref='tournament', lazy=True)
    
    def __init__(self, name, start_date, end_date, description=None, logo_url=None, status='upcoming'):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.logo_url = logo_url
        self.status = status

class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Group Stage", "Quarter Finals", "Semi Finals", "Final"
    sequence = db.Column(db.Integer, nullable=False)  # Order of stages: 1, 2, 3...
    stage_type = db.Column(db.String(20), nullable=False)  # league, knockout, round-robin, etc.
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, completed
    
    groups = db.relationship('Group', backref='stage', lazy=True)
    matches = db.relationship('Match', backref='stage', lazy=True)
    
    def __init__(self, tournament_id, name, sequence, stage_type, 
                 start_date=None, end_date=None, status='upcoming'):
        self.tournament_id = tournament_id
        self.name = name
        self.sequence = sequence
        self.stage_type = stage_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Group A", "Group B"
    
    group_teams = db.relationship('GroupTeam', backref='group', lazy=True)
    
    def __init__(self, stage_id, name):
        self.stage_id = stage_id
        self.name = name

class GroupTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    
    # Points table statistics
    played = db.Column(db.Integer, default=0)
    won = db.Column(db.Integer, default=0)
    lost = db.Column(db.Integer, default=0)
    tied = db.Column(db.Integer, default=0)
    no_result = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    net_run_rate = db.Column(db.Float, default=0.0)
    
    # Additional stats for detailed view
    runs_scored = db.Column(db.Integer, default=0)
    runs_conceded = db.Column(db.Integer, default=0)
    overs_played = db.Column(db.Float, default=0.0)
    overs_bowled = db.Column(db.Float, default=0.0)
    
    def __init__(self, group_id, team_id):
        self.group_id = group_id
        self.team_id = team_id

# Update existing Match model with tournament-related fields
# Add these columns to your existing Match model
"""
stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
match_number = db.Column(db.Integer)  # e.g., Match #1, Match #2
is_knockout = db.Column(db.Boolean, default=False)
"""

# Marshmallow Schemas for serialization
class TournamentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tournament

class StageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stage
        include_fk = True

class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        include_fk = True

class GroupTeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupTeam
        include_fk = True

# Initialize schemas
tournament_schema = TournamentSchema()
tournaments_schema = TournamentSchema(many=True)
stage_schema = StageSchema()
stages_schema = StageSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
group_team_schema = GroupTeamSchema()
group_teams_schema = GroupTeamSchema(many=True)

# Routes for Tournaments
@app.route('/api/tournaments', methods=['POST'])
def add_tournament():
    name = request.json['name']
    start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d')
    description = request.json.get('description')
    logo_url = request.json.get('logo_url')
    status = request.json.get('status', 'upcoming')
    
    new_tournament = Tournament(name, start_date, end_date, description, logo_url, status)
    db.session.add(new_tournament)
    db.session.commit()
    
    return tournament_schema.jsonify(new_tournament)

@app.route('/api/tournaments', methods=['GET'])
def get_tournaments():
    all_tournaments = Tournament.query.all()
    return tournaments_schema.jsonify(all_tournaments)

@app.route('/api/tournaments/<id>', methods=['GET'])
def get_tournament(id):
    tournament = Tournament.query.get_or_404(id)
    return tournament_schema.jsonify(tournament)

@app.route('/api/tournaments/<id>', methods=['PUT'])
def update_tournament(id):
    tournament = Tournament.query.get_or_404(id)
    
    tournament.name = request.json.get('name', tournament.name)
    
    if 'start_date' in request.json:
        tournament.start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d')
    
    if 'end_date' in request.json:
        tournament.end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d')
    
    tournament.description = request.json.get('description', tournament.description)
    tournament.logo_url = request.json.get('logo_url', tournament.logo_url)
    tournament.status = request.json.get('status', tournament.status)
    
    db.session.commit()
    return tournament_schema.jsonify(tournament)

@app.route('/api/tournaments/<id>', methods=['DELETE'])
def delete_tournament(id):
    tournament = Tournament.query.get_or_404(id)
    db.session.delete(tournament)
    db.session.commit()
    return jsonify({'message': 'Tournament deleted successfully'})

# Routes for Stages
@app.route('/api/tournaments/<tournament_id>/stages', methods=['POST'])
def add_stage(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    
    name = request.json['name']
    sequence = request.json['sequence']
    stage_type = request.json['stage_type']
    
    start_date = None
    if 'start_date' in request.json:
        start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d')
    
    end_date = None
    if 'end_date' in request.json:
        end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d')
    
    status = request.json.get('status', 'upcoming')
    
    new_stage = Stage(tournament_id, name, sequence, stage_type, start_date, end_date, status)
    db.session.add(new_stage)
    db.session.commit()
    
    return stage_schema.jsonify(new_stage)

@app.route('/api/tournaments/<tournament_id>/stages', methods=['GET'])
def get_tournament_stages(tournament_id):
    stages = Stage.query.filter_by(tournament_id=tournament_id).order_by(Stage.sequence).all()
    return stages_schema.jsonify(stages)

@app.route('/api/stages/<id>', methods=['GET'])
def get_stage(id):
    stage = Stage.query.get_or_404(id)
    return stage_schema.jsonify(stage)

@app.route('/api/stages/<id>', methods=['PUT'])
def update_stage(id):
    stage = Stage.query.get_or_404(id)
    
    stage.name = request.json.get('name', stage.name)
    stage.sequence = request.json.get('sequence', stage.sequence)
    stage.stage_type = request.json.get('stage_type', stage.stage_type)
    
    if 'start_date' in request.json:
        stage.start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d')
    
    if 'end_date' in request.json:
        stage.end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d')
    
    stage.status = request.json.get('status', stage.status)
    
    db.session.commit()
    return stage_schema.jsonify(stage)

# Routes for Groups
@app.route('/api/stages/<stage_id>/groups', methods=['POST'])
def add_group(stage_id):
    stage = Stage.query.get_or_404(stage_id)
    
    name = request.json['name']
    
    new_group = Group(stage_id, name)
    db.session.add(new_group)
    db.session.commit()
    
    return group_schema.jsonify(new_group)

@app.route('/api/stages/<stage_id>/groups', methods=['GET'])
def get_stage_groups(stage_id):
    groups = Group.query.filter_by(stage_id=stage_id).all()
    return groups_schema.jsonify(groups)

@app.route('/api/groups/<id>', methods=['GET'])
def get_group(id):
    group = Group.query.get_or_404(id)
    return group_schema.jsonify(group)

# Routes for adding teams to groups
@app.route('/api/groups/<group_id>/teams', methods=['POST'])
def add_team_to_group(group_id):
    group = Group.query.get_or_404(group_id)
    
    team_id = request.json['team_id']
    
    # Check if team already exists in this group
    existing_entry = GroupTeam.query.filter_by(group_id=group_id, team_id=team_id).first()
    if existing_entry:
        return jsonify({'message': 'Team already exists in this group'}), 400
    
    new_group_team = GroupTeam(group_id, team_id)
    db.session.add(new_group_team)
    db.session.commit()
    
    return group_team_schema.jsonify(new_group_team)

@app.route('/api/groups/<group_id>/teams', methods=['GET'])
def get_group_teams(group_id):
    group_teams = GroupTeam.query.filter_by(group_id=group_id).all()
    return group_teams_schema.jsonify(group_teams)

# Route for group points table
@app.route('/api/groups/<group_id>/points-table', methods=['GET'])
def get_group_points_table(group_id):
    group = Group.query.get_or_404(group_id)
    group_teams = GroupTeam.query.filter_by(group_id=group_id).all()
    
    points_table = []
    for group_team in group_teams:
        team = Team.query.get(group_team.team_id)
        team_data = {
            'team_id': team.id,
            'team_name': team.name,
            'played': group_team.played,
            'won': group_team.won,
            'lost': group_team.lost,
            'tied': group_team.tied,
            'no_result': group_team.no_result,
            'points': group_team.points,
            'net_run_rate': round(group_team.net_run_rate, 3)
        }
        points_table.append(team_data)
    
    # Sort by points (descending), then by net run rate (descending)
    points_table = sorted(points_table, key=lambda x: (x['points'], x['net_run_rate']), reverse=True)
    
    return jsonify({
        'group_name': group.name,
        'standings': points_table
    })

# Route for creating matches within a stage/group
@app.route('/api/stages/<stage_id>/matches', methods=['POST'])
def add_stage_match(stage_id):
    stage = Stage.query.get_or_404(stage_id)
    
    team1_id = request.json['team1_id']
    team2_id = request.json['team2_id']
    venue = request.json['venue']
    match_date = datetime.strptime(request.json['match_date'], '%Y-%m-%d %H:%M:%S')
    match_type = request.json['match_type']
    overs = request.json['overs']
    status = request.json.get('status', 'scheduled')
    group_id = request.json.get('group_id')
    match_number = request.json.get('match_number')
    is_knockout = request.json.get('is_knockout', False)
    
    # Create new match
    new_match = Match(team1_id, team2_id, venue, match_date, match_type, overs, status)
    new_match.stage_id = stage_id
    new_match.group_id = group_id
    new_match.match_number = match_number
    new_match.is_knockout = is_knockout
    
    db.session.add(new_match)
    db.session.commit()
    
    return match_schema.jsonify(new_match)

@app.route('/api/stages/<stage_id>/matches', methods=['GET'])
def get_stage_matches(stage_id):
    matches = Match.query.filter_by(stage_id=stage_id).all()
    return matches_schema.jsonify(matches)

@app.route('/api/groups/<group_id>/matches', methods=['GET'])
def get_group_matches(group_id):
    matches = Match.query.filter_by(group_id=group_id).all()
    return matches_schema.jsonify(matches)

# Update group statistics and points table after a match
@app.route('/api/matches/<match_id>/update-points-table', methods=['POST'])
def update_points_table(match_id):
    match = Match.query.get_or_404(match_id)
    
    # Only update points if the match is completed and belongs to a group
    if match.status != 'completed' or not match.group_id:
        return jsonify({'message': 'Match not completed or not part of a group'}), 400
    
    # Get the winner team ID
    winner_id = match.winner
    
    # Get team entries in the group
    team1_group = GroupTeam.query.filter_by(group_id=match.group_id, team_id=match.team1_id).first()
    team2_group = GroupTeam.query.filter_by(group_id=match.group_id, team_id=match.team2_id).first()
    
    if not team1_group or not team2_group:
        return jsonify({'message': 'Teams not found in group'}), 400
    
    # Update matches played
    team1_group.played += 1
    team2_group.played += 1
    
    # Get innings data for run rate calculations
    innings_list = Innings.query.filter_by(match_id=match_id).all()
    
    team1_runs_scored = 0
    team1_runs_conceded = 0
    team1_overs_played = 0.0
    team1_overs_bowled = 0.0
    
    team2_runs_scored = 0
    team2_runs_conceded = 0
    team2_overs_played = 0.0
    team2_overs_bowled = 0.0
    
    for innings in innings_list:
        if innings.batting_team_id == match.team1_id:
            team1_runs_scored += innings.total_runs
            team1_overs_played += innings.total_overs
            team2_overs_bowled += innings.total_overs
        elif innings.batting_team_id == match.team2_id:
            team2_runs_scored += innings.total_runs
            team2_overs_played += innings.total_overs
            team1_overs_bowled += innings.total_overs
    
    team1_runs_conceded = team2_runs_scored
    team2_runs_conceded = team1_runs_scored
    
    # Update run stats
    team1_group.runs_scored += team1_runs_scored
    team1_group.runs_conceded += team1_runs_conceded
    team1_group.overs_played += team1_overs_played
    team1_group.overs_bowled += team1_overs_bowled
    
    team2_group.runs_scored += team2_runs_scored
    team2_group.runs_conceded += team2_runs_conceded
    team2_group.overs_played += team2_overs_played
    team2_group.overs_bowled += team2_overs_bowled
    
    # Match result scenarios
    if winner_id == match.team1_id:
        # Team 1 won
        team1_group.won += 1
        team1_group.points += 2  # 2 points for a win
        team2_group.lost += 1
    elif winner_id == match.team2_id:
        # Team 2 won
        team2_group.won += 1
        team2_group.points += 2  # 2 points for a win
        team1_group.lost += 1
    elif winner_id == 0:  # Use 0 for tied matches
        # Match tied
        team1_group.tied += 1
        team2_group.tied += 1
        team1_group.points += 1  # 1 point for a tie
        team2_group.points += 1  # 1 point for a tie
    else:
        # No result
        team1_group.no_result += 1
        team2_group.no_result += 1
        team1_group.points += 1  # 1 point for no result
        team2_group.points += 1  # 1 point for no result
    
    # Calculate net run rate
    # NRR = (Total runs scored / Total overs faced) - (Total runs conceded / Total overs bowled)
    if team1_group.overs_played > 0 and team1_group.overs_bowled > 0:
        team1_group.net_run_rate = (team1_group.runs_scored / convert_to_balls(team1_group.overs_played) * 6) - \
                                 (team1_group.runs_conceded / convert_to_balls(team1_group.overs_bowled) * 6)
    
    if team2_group.overs_played > 0 and team2_group.overs_bowled > 0:
        team2_group.net_run_rate = (team2_group.runs_scored / convert_to_balls(team2_group.overs_played) * 6) - \
                                 (team2_group.runs_conceded / convert_to_balls(team2_group.overs_bowled) * 6)
    
    db.session.commit()
    
    return jsonify({'message': 'Points table updated successfully'})

# Helper function to convert overs to balls
def convert_to_balls(overs):
    whole_overs = int(overs)
    balls = (overs - whole_overs) * 10
    return whole_overs * 6 + balls

# Route to get tournament brackets for knockout stages
@app.route('/api/tournaments/<tournament_id>/bracket', methods=['GET'])
def get_tournament_bracket(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    stages = Stage.query.filter_by(tournament_id=tournament_id, stage_type='knockout').order_by(Stage.sequence).all()
    
    if not stages:
        return jsonify({'message': 'No knockout stages found for this tournament'}), 404
    
    bracket = {
        'tournament_name': tournament.name,
        'stages': []
    }
    
    for stage in stages:
        stage_data = {
            'stage_name': stage.name,
            'matches': []
        }
        
        matches = Match.query.filter_by(stage_id=stage.id).all()
        for match in matches:
            team1 = Team.query.get(match.team1_id)
            team2 = Team.query.get(match.team2_id)
            winner = None
            if match.winner:
                winner = Team.query.get(match.winner)
            
            match_data = {
                'match_id': match.id,
                'match_number': match.match_number,
                'team1': team1.name,
                'team2': team2.name,
                'venue': match.venue,
                'date': match.match_date.strftime('%Y-%m-%d %H:%M'),
                'status': match.status,
                'winner': winner.name if winner else None
            }
            stage_data['matches'].append(match_data)
        
        bracket['stages'].append(stage_data)
    
    return jsonify(bracket)

# Tournament statistics endpoint
@app.route('/api/tournaments/<tournament_id>/stats', methods=['GET'])
def get_tournament_stats(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    
    # Get all matches in this tournament
    matches = Match.query.join(Stage).filter(Stage.tournament_id == tournament_id).all()
    
    # Top run scorers
    batting_stats = db.session.query(
        Player.id,
        Player.name,
        db.func.sum(BattingStats.runs).label('total_runs'),
        db.func.sum(BattingStats.balls_faced).label('balls_faced'),
        db.func.sum(BattingStats.fours).label('fours'),
        db.func.sum(BattingStats.sixes).label('sixes')
    ).join(BattingStats, Player.id == BattingStats.player_id)\
     .join(Innings, BattingStats.innings_id == Innings.id)\
     .join(Match, Innings.match_id == Match.id)\
     .join(Stage, Match.stage_id == Stage.id)\
     .filter(Stage.tournament_id == tournament_id)\
     .group_by(Player.id)\
     .order_by(db.desc('total_runs'))\
     .limit(10).all()
    
    # Top wicket takers
    bowling_stats = db.session.query(
        Player.id,
        Player.name,
        db.func.sum(BowlingStats.wickets).label('total_wickets'),
        db.func.sum(BowlingStats.runs_given).label('runs_given'),
        db.func.sum(BowlingStats.overs).label('overs')
    ).join(BowlingStats, Player.id == BowlingStats.player_id)\
     .join(Innings, BowlingStats.innings_id == Innings.id)\
     .join(Match, Innings.match_id == Match.id)\
     .join(Stage, Match.stage_id == Stage.id)\
     .filter(Stage.tournament_id == tournament_id)\
     .group_by(Player.id)\
     .order_by(db.desc('total_wickets'))\
     .limit(10).all()
    
    # Highest team scores
    highest_scores = db.session.query(
        Innings.id,
        Team.name,
        Innings.total_runs,
        Innings.total_wickets,
        Innings.total_overs,
        Match.venue
    ).join(Team, Innings.batting_team_id == Team.id)\
     .join(Match, Innings.match_id == Match.id)\
     .join(Stage, Match.stage_id == Stage.id)\
     .filter(Stage.tournament_id == tournament_id)\
     .order_by(db.desc(Innings.total_runs))\
     .limit(5).all()
    
    stats = {
        'tournament_name': tournament.name,
        'total_matches': len(matches),
        'completed_matches': len([m for m in matches if m.status == 'completed']),
        'remaining_matches': len([m for m in matches if m.status != 'completed']),
        'top_run_scorers': [
            {
                'player_name': stat[1],
                'runs': stat[2],
                'strike_rate': round((stat[2] / stat[3]) * 100, 2) if stat[3] > 0 else 0,
                'fours': stat[4],
                'sixes': stat[5]
            } for stat in batting_stats
        ],
        'top_wicket_takers': [
            {
                'player_name': stat[1],
                'wickets': stat[2],
                'economy': round(stat[3] / stat[4], 2) if stat[4] > 0 else 0
            } for stat in bowling_stats
        ],
        'highest_team_scores': [
            {
                'team_name': stat[1],
                'score': f"{stat[2]}/{stat[3]}",
                'overs': stat[4],
                'venue': stat[5]
            } for stat in highest_scores
        ]
    }
    
    return jsonify(stats)