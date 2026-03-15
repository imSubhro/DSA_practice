from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cricket.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(255))
    players = db.relationship('Player', backref='team', lazy=True)
    
    def __init__(self, name, logo_url=None):
        self.name = name
        self.logo_url = logo_url

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    jersey_number = db.Column(db.Integer)
    role = db.Column(db.String(50))  # batsman, bowler, all-rounder, wicket-keeper
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    # Specify foreign_keys to avoid ambiguity
    batting_stats = db.relationship('BattingStats', backref='batsman', lazy=True, foreign_keys='[BattingStats.player_id]')
    bowling_dismissals = db.relationship('BattingStats', backref='bowler', lazy=True, foreign_keys='[BattingStats.bowler_id]')
    fielding_dismissals = db.relationship('BattingStats', backref='fielder', lazy=True, foreign_keys='[BattingStats.fielder_id]')

    def __init__(self, name, jersey_number, role, team_id):
        self.name = name
        self.jersey_number = jersey_number
        self.role = role
        self.team_id = team_id

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    venue = db.Column(db.String(100))
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    match_type = db.Column(db.String(50))  # T20, ODI, Test
    overs = db.Column(db.Integer)
    status = db.Column(db.String(50), default='scheduled')  # scheduled, in-progress, completed
    toss_winner = db.Column(db.Integer, db.ForeignKey('team.id'))
    toss_decision = db.Column(db.String(10))  # bat, field
    winner = db.Column(db.Integer, db.ForeignKey('team.id'))
    innings = db.relationship('Innings', backref='match', lazy=True)
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    match_number = db.Column(db.Integer)  # e.g., Match #1, Match #2
    is_knockout = db.Column(db.Boolean, default=False)
    
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])
    
    def __init__(self, team1_id, team2_id, venue, match_date, match_type, overs, status='scheduled'):
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.venue = venue
        self.match_date = match_date
        self.match_type = match_type
        self.overs = overs
        self.status = status

class Innings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    batting_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    bowling_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    innings_number = db.Column(db.Integer, nullable=False)  # 1 or 2
    total_runs = db.Column(db.Integer, default=0)
    total_wickets = db.Column(db.Integer, default=0)
    total_overs = db.Column(db.Float, default=0.0)  # 6.2 means 6 overs and 2 balls
    extras = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='in-progress')  # in-progress, completed
    
    batting_team = db.relationship('Team', foreign_keys=[batting_team_id])
    bowling_team = db.relationship('Team', foreign_keys=[bowling_team_id])
    batting_stats = db.relationship('BattingStats', backref='innings', lazy=True)
    bowling_stats = db.relationship('BowlingStats', backref='innings', lazy=True)
    balls = db.relationship('Ball', backref='innings', lazy=True)
    
    def __init__(self, match_id, batting_team_id, bowling_team_id, innings_number):
        self.match_id = match_id
        self.batting_team_id = batting_team_id
        self.bowling_team_id = bowling_team_id
        self.innings_number = innings_number

class BattingStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)  # Batsman
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    runs = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    dismissal_type = db.Column(db.String(50))  # bowled, caught, lbw, etc.
    
    bowler_id = db.Column(db.Integer, db.ForeignKey('player.id'))  # Bowler
    fielder_id = db.Column(db.Integer, db.ForeignKey('player.id'))  # Fielder

    def __init__(self, player_id, innings_id):
        self.player_id = player_id
        self.innings_id = innings_id


class BowlingStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    overs = db.Column(db.Float, default=0.0)
    runs_given = db.Column(db.Integer, default=0)
    wickets = db.Column(db.Integer, default=0)
    maidens = db.Column(db.Integer, default=0)
    no_balls = db.Column(db.Integer, default=0)
    wides = db.Column(db.Integer, default=0)
    
    def __init__(self, player_id, innings_id):
        self.player_id = player_id
        self.innings_id = innings_id

class Ball(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    over_number = db.Column(db.Integer, nullable=False)
    ball_number = db.Column(db.Integer, nullable=False)  # 1-6
    batsman_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    bowler_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    runs_scored = db.Column(db.Integer, default=0)
    is_extra = db.Column(db.Boolean, default=False)
    extra_type = db.Column(db.String(10))  # wide, no-ball, bye, leg-bye
    extra_runs = db.Column(db.Integer, default=0)
    is_wicket = db.Column(db.Boolean, default=False)
    wicket_type = db.Column(db.String(50))  # bowled, caught, lbw, etc.
    fielder_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    
    def __init__(self, innings_id, over_number, ball_number, batsman_id, bowler_id):
        self.innings_id = innings_id
        self.over_number = over_number
        self.ball_number = ball_number
        self.batsman_id = batsman_id
        self.bowler_id = bowler_id

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

# Marshmallow Schemas for serialization
class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team

class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        include_fk = True

class MatchSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Match
        include_fk = True

class InningsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Innings
        include_fk = True

class BattingStatsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BattingStats
        include_fk = True

class BowlingStatsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BowlingStats
        include_fk = True

class BallSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ball
        include_fk = True

class TournamentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tournament

class StageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Stage
        include_fk = True

class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        include_fk = True

class GroupTeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GroupTeam
        include_fk = True


# Initialize schemas
team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)
match_schema = MatchSchema()
matches_schema = MatchSchema(many=True)
innings_schema = InningsSchema()
innings_list_schema = InningsSchema(many=True)
batting_stats_schema = BattingStatsSchema()
batting_stats_list_schema = BattingStatsSchema(many=True)
bowling_stats_schema = BowlingStatsSchema()
bowling_stats_list_schema = BowlingStatsSchema(many=True)
ball_schema = BallSchema()
balls_schema = BallSchema(many=True)
tournament_schema = TournamentSchema()
tournaments_schema = TournamentSchema(many=True)
stage_schema = StageSchema()
stages_schema = StageSchema(many=True)
group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
group_team_schema = GroupTeamSchema()
group_teams_schema = GroupTeamSchema(many=True)

# Routes for Teams
@app.route('/api/teams', methods=['POST'])
def add_team():
    name = request.json['name']
    logo_url = request.json.get('logo_url')
    
    new_team = Team(name, logo_url)
    db.session.add(new_team)
    db.session.commit()
    
    # return team_schema.jsonify(new_team)
    return jsonify(team_schema.dump(new_team))


@app.route('/api/teams', methods=['GET'])
def get_teams():
    all_teams = Team.query.all()
    return teams_schema.jsonify(all_teams)

@app.route('/api/teams/<id>', methods=['GET'])
def get_team(id):
    team = Team.query.get_or_404(id)
    return team_schema.jsonify(team)

@app.route('/api/teams/<id>', methods=['PUT'])
def update_team(id):
    team = Team.query.get_or_404(id)
    
    name = request.json.get('name', team.name)
    logo_url = request.json.get('logo_url', team.logo_url)
    
    team.name = name
    team.logo_url = logo_url
    
    db.session.commit()
    return team_schema.jsonify(team)

@app.route('/api/teams/<id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({'message': 'Team deleted successfully'})

# Routes for Players
@app.route('/api/players', methods=['POST'])
def add_player():
    name = request.json['name']
    jersey_number = request.json['jersey_number']
    role = request.json['role']
    team_id = request.json['team_id']
    
    new_player = Player(name, jersey_number, role, team_id)
    db.session.add(new_player)
    db.session.commit()
    
    # return player_schema.jsonify(new_player)
    return jsonify(player_schema.dump(new_player))

@app.route('/api/players', methods=['GET'])
def get_players():
    all_players = Player.query.all()
    # return players_schema.jsonify(all_players)
    return jsonify(player_schema.dump(all_players))

@app.route('/api/players/<id>', methods=['GET'])
def get_player(id):
    player = Player.query.get_or_404(id)
    # return player_schema.jsonify(player)
    return jsonify(player_schema.dump(player))

@app.route('/api/teams/<team_id>/players', methods=['GET'])
def get_team_players(team_id):
    team_players = Player.query.filter_by(team_id=team_id).all()
    return players_schema.jsonify(team_players)

@app.route('/api/players/<id>', methods=['PUT'])
def update_player(id):
    player = Player.query.get_or_404(id)
    
    player.name = request.json.get('name', player.name)
    player.jersey_number = request.json.get('jersey_number', player.jersey_number)
    player.role = request.json.get('role', player.role)
    player.team_id = request.json.get('team_id', player.team_id)
    
    db.session.commit()
    return player_schema.jsonify(player)

@app.route('/api/players/<id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player deleted successfully'})

# Routes for Matches
@app.route('/api/matches', methods=['POST'])
def add_match():
    team1_id = request.json['team1_id']
    team2_id = request.json['team2_id']
    venue = request.json['venue']
    match_date = datetime.strptime(request.json['match_date'], '%Y-%m-%d %H:%M:%S')
    match_type = request.json['match_type']
    overs = request.json['overs']
    status = request.json.get('status', 'scheduled')
    
    new_match = Match(team1_id, team2_id, venue, match_date, match_type, overs, status)
    db.session.add(new_match)
    db.session.commit()
    
    # return match_schema.jsonify(new_match)
    return jsonify(match_schema.dump(new_match))

@app.route('/api/matches', methods=['GET'])
def get_matches():
    all_matches = Match.query.all()
    # return matches_schema.jsonify(all_matches)
    return jsonify(match_schema.dump(all_matches))

@app.route('/api/matches/<id>', methods=['GET'])
def get_match(id):
    match = Match.query.get_or_404(id)
    # return match_schema.jsonify(match)
    return jsonify(match_schema.dump(match))

@app.route('/api/matches/<id>/toss', methods=['PUT'])
def update_toss(id):
    match = Match.query.get_or_404(id)
    
    match.toss_winner = request.json['toss_winner']
    match.toss_decision = request.json['toss_decision']
    match.status = 'in-progress'
    
    db.session.commit()
    # return match_schema.jsonify(match)
    return jsonify(match_schema.dump(match))

@app.route('/api/matches/<id>/status', methods=['PUT'])
def update_match_status(id):
    match = Match.query.get_or_404(id)
    
    match.status = request.json['status']
    if request.json['status'] == 'completed':
        match.winner = request.json.get('winner')
    
    db.session.commit()
    # return match_schema.jsonify(match)
    return jsonify(match_schema.dump(match))

# Routes for Innings
@app.route('/api/matches/<match_id>/innings', methods=['POST'])
def add_innings(match_id):
    match = Match.query.get_or_404(match_id)
    
    batting_team_id = request.json['batting_team_id']
    bowling_team_id = request.json['bowling_team_id']
    innings_number = request.json['innings_number']
    
    new_innings = Innings(match_id, batting_team_id, bowling_team_id, innings_number)
    db.session.add(new_innings)
    db.session.commit()
    
    # return innings_schema.jsonify(new_innings)
    return jsonify(innings_schema.dump(new_innings))

@app.route('/api/matches/<match_id>/innings', methods=['GET'])
def get_match_innings(match_id):
    innings_list = Innings.query.filter_by(match_id=match_id).all()
    return innings_list_schema.jsonify(innings_list)

@app.route('/api/innings/<innings_id>', methods=['GET'])
def get_innings(innings_id):
    innings = Innings.query.get_or_404(innings_id)
    return innings_schema.jsonify(innings)

@app.route('/api/innings/<innings_id>/batting-stats', methods=['POST'])
def add_batting_stats(innings_id):
    player_id = request.json['player_id']
    
    # Check if stats already exist for this player in this innings
    existing_stats = BattingStats.query.filter_by(player_id=player_id, innings_id=innings_id).first()
    if existing_stats:
        return jsonify({'message': 'Batting stats already exist for this player in this innings'}), 400
    
    new_batting_stats = BattingStats(player_id, innings_id)
    db.session.add(new_batting_stats)
    db.session.commit()
    
    # return batting_stats_schema.jsonify(new_batting_stats)
    return jsonify(batting_stats_schema.dump(new_batting_stats))

@app.route('/api/innings/<innings_id>/bowling-stats', methods=['POST'])
def add_bowling_stats(innings_id):
    
    player_id = request.json['player_id']
    
    # Check if stats already exist for this player in this innings
    existing_stats = BowlingStats.query.filter_by(player_id=player_id, innings_id=innings_id).first()
    if existing_stats:
        return jsonify({'message': 'Bowling stats already exist for this player in this innings'}), 400
    
    new_bowling_stats = BowlingStats(player_id, innings_id)
    db.session.add(new_bowling_stats)
    db.session.commit()
    
    # return bowling_stats_schema.jsonify(new_bowling_stats)
    return jsonify(bowling_stats_schema.dump(new_bowling_stats))

@app.route('/api/innings/<innings_id>/batting-stats', methods=['GET'])
def get_innings_batting_stats(innings_id):
    batting_stats = BattingStats.query.filter_by(innings_id=innings_id).all()
    return batting_stats_list_schema.jsonify(batting_stats)

@app.route('/api/innings/<innings_id>/bowling-stats', methods=['GET'])
def get_innings_bowling_stats(innings_id):
    bowling_stats = BowlingStats.query.filter_by(innings_id=innings_id).all()
    return bowling_stats_list_schema.jsonify(bowling_stats)

# Routes for Ball-by-Ball scoring
@app.route('/api/innings/<innings_id>/balls', methods=['POST'])
def add_ball(innings_id):
    innings = Innings.query.get_or_404(innings_id)
    
    over_number = request.json['over_number']
    ball_number = request.json['ball_number']
    batsman_id = request.json['batsman_id']
    bowler_id = request.json['bowler_id']
    runs_scored = request.json.get('runs_scored', 0)
    is_extra = request.json.get('is_extra', False)
    extra_type = request.json.get('extra_type')
    extra_runs = request.json.get('extra_runs', 0)
    is_wicket = request.json.get('is_wicket', False)
    wicket_type = request.json.get('wicket_type')
    fielder_id = request.json.get('fielder_id')
    
    # Create new ball
    new_ball = Ball(innings_id, over_number, ball_number, batsman_id, bowler_id)
    new_ball.runs_scored = runs_scored
    new_ball.is_extra = is_extra
    new_ball.extra_type = extra_type
    new_ball.extra_runs = extra_runs
    new_ball.is_wicket = is_wicket
    new_ball.wicket_type = wicket_type
    new_ball.fielder_id = fielder_id
    
    db.session.add(new_ball)
    
    # Update batting stats
    batting_stats = BattingStats.query.filter_by(player_id=batsman_id, innings_id=innings_id).first()
    if batting_stats:
        batting_stats.runs += runs_scored
        
        # Only count legitimate deliveries as balls faced
        if not is_extra or extra_type in ['no-ball']:
            batting_stats.balls_faced += 1
        
        # Update 4s and 6s
        if runs_scored == 4:
            batting_stats.fours += 1
        elif runs_scored == 6:
            batting_stats.sixes += 1
        
        # Update dismissal details if out
        if is_wicket:
            batting_stats.dismissal_type = wicket_type
            batting_stats.bowler_id = bowler_id
            batting_stats.fielder_id = fielder_id
    
    # Update bowling stats
    bowling_stats = BowlingStats.query.filter_by(player_id=bowler_id, innings_id=innings_id).first()
    if bowling_stats:
        # Update overs bowled (for valid deliveries)
        if not is_extra or extra_type in ['bye', 'leg-bye']:
            current_balls = int(bowling_stats.overs * 10) % 10
            current_overs = int(bowling_stats.overs)
            
            if current_balls == 5:
                bowling_stats.overs = current_overs + 1
            else:
                bowling_stats.overs = current_overs + (current_balls + 1) / 10
        
        # Update runs conceded
        total_runs = runs_scored + extra_runs
        if extra_type not in ['bye', 'leg-bye']:  # These aren't charged to the bowler
            bowling_stats.runs_given += total_runs
            
        # Update extras
        if is_extra:
            if extra_type == 'wide':
                bowling_stats.wides += 1
            elif extra_type == 'no-ball':
                bowling_stats.no_balls += 1
        
        # Update wickets
        if is_wicket and wicket_type not in ['run-out', 'retired-hurt', 'timed-out', 'obstructing-field']:
            bowling_stats.wickets += 1
    
    # Update innings totals
    innings.total_runs += (runs_scored + extra_runs)
    
    # Update overs
    if not is_extra or extra_type in ['bye', 'leg-bye', 'no-ball']:
        current_balls = int(innings.total_overs * 10) % 10
        current_overs = int(innings.total_overs)
        
        if current_balls == 5:
            innings.total_overs = current_overs + 1
        else:
            innings.total_overs = current_overs + (current_balls + 1) / 10
    
    # Update wickets
    if is_wicket:
        innings.total_wickets += 1
    
    # Update extras
    if is_extra:
        innings.extras += extra_runs
    
    db.session.commit()
    
    # return ball_schema.jsonify(new_ball)
    return jsonify(ball_schema.dump(new_ball))

@app.route('/api/innings/<innings_id>/balls', methods=['GET'])
def get_innings_balls(innings_id):
    balls = Ball.query.filter_by(innings_id=innings_id).order_by(Ball.over_number, Ball.ball_number).all()
    return balls_schema.jsonify(balls)

@app.route('/api/innings/<innings_id>/score', methods=['GET'])
def get_innings_score(innings_id):
    innings = Innings.query.get_or_404(innings_id)
    
    score_data = {
        'total_runs': innings.total_runs,
        'total_wickets': innings.total_wickets,
        'total_overs': innings.total_overs,
        'extras': innings.extras,
        'run_rate': round(innings.total_runs / innings.total_overs, 2) if innings.total_overs > 0 else 0
    }
    
    return jsonify(score_data)

@app.route('/api/matches/<match_id>/scorecard', methods=['GET'])
def get_match_scorecard(match_id):
    match = Match.query.get_or_404(match_id)
    innings_list = Innings.query.filter_by(match_id=match_id).all()
    
    scorecard = {
        'match_details': {
            'id': match.id,
            'team1': match.team1.name,
            'team2': match.team2.name,
            'venue': match.venue,
            'match_date': match.match_date,
            'match_type': match.match_type,
            'status': match.status
        },
        'innings': []
    }
    
    for innings in innings_list:
        innings_data = {
            'innings_number': innings.innings_number,
            'batting_team': innings.batting_team.name,
            'bowling_team': innings.bowling_team.name,
            'total_score': f"{innings.total_runs}/{innings.total_wickets}",
            'total_overs': innings.total_overs,
            'extras': innings.extras,
            'run_rate': round(innings.total_runs / innings.total_overs, 2) if innings.total_overs > 0 else 0,
            'batting': [],
            'bowling': []
        }
        
        # Add batting stats
        batting_stats = BattingStats.query.filter_by(innings_id=innings.id).all()
        for stat in batting_stats:
            player = Player.query.get(stat.player_id)
            bat_stat = {
                'player_name': player.name,
                'runs': stat.runs,
                'balls': stat.balls_faced,
                'fours': stat.fours,
                'sixes': stat.sixes,
                'strike_rate': round((stat.runs / stat.balls_faced) * 100, 2) if stat.balls_faced > 0 else 0,
                'dismissal': stat.dismissal_type
            }
            innings_data['batting'].append(bat_stat)
        
        # Add bowling stats
        bowling_stats = BowlingStats.query.filter_by(innings_id=innings.id).all()
        for stat in bowling_stats:
            player = Player.query.get(stat.player_id)
            bowl_stat = {
                'player_name': player.name,
                'overs': stat.overs,
                'runs': stat.runs_given,
                'wickets': stat.wickets,
                'maidens': stat.maidens,
                'economy': round(stat.runs_given / stat.overs, 2) if stat.overs > 0 else 0,
                'wides': stat.wides,
                'no_balls': stat.no_balls
            }
            innings_data['bowling'].append(bowl_stat)
        
        scorecard['innings'].append(innings_data)
    
    return jsonify(scorecard)

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
    
    return jsonify(tournament_schema.dump(new_tournament))


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
    # return tournament_schema.jsonify(tournament)
    return jsonify(tournament_schema.dump(tournament))

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
    
    # return stage_schema.jsonify(new_stage)
    return jsonify(stage_schema.dump(new_stage))

@app.route('/api/tournaments/<tournament_id>/stages', methods=['GET'])
def get_tournament_stages(tournament_id):
    stages = Stage.query.filter_by(tournament_id=tournament_id).order_by(Stage.sequence).all()
    # return stages_schema.jsonify(stages)
    return jsonify(stages_schema.dump(stages))

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
    
    # return group_schema.jsonify(new_group)
    return jsonify(group_schema.dump(new_group))

@app.route('/api/stages/<stage_id>/groups', methods=['GET'])
def get_stage_groups(stage_id):
    groups = Group.query.filter_by(stage_id=stage_id).all()
    # return groups_schema.jsonify(groups)
    return jsonify(groups_schema.dump(groups))

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
    
    # return group_team_schema.jsonify(new_group_team)
    return jsonify(group_team_schema.dump(new_group_team))

@app.route('/api/groups/<group_id>/teams', methods=['GET'])
def get_group_teams(group_id):
    group_teams = GroupTeam.query.filter_by(group_id=group_id).all()
    # return group_teams_schema.jsonify(group_teams)
    return jsonify(group_teams_schema.dump(group_teams))

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
    
    # return match_schema.jsonify(new_match)
    return jsonify(match_schema.dump(new_match))

@app.route('/api/stages/<stage_id>/matches', methods=['GET'])
def get_stage_matches(stage_id):
    matches = Match.query.filter_by(stage_id=stage_id).all()
    # return matches_schema.jsonify(matches)
    return jsonify(matches_schema.dump(matches))

@app.route('/api/groups/<group_id>/matches', methods=['GET'])
def get_group_matches(group_id):
    matches = Match.query.filter_by(group_id=group_id).all()
    # return matches_schema.jsonify(matches)
    return jsonify(matches_schema.dump(matches))

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


# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    #marshmallow-sqlalchemy
