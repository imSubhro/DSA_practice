from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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
    batting_stats = db.relationship('BattingStats', backref='player', lazy=True)
    bowling_stats = db.relationship('BowlingStats', backref='player', lazy=True)
    
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
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    runs = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    dismissal_type = db.Column(db.String(50))  # bowled, caught, lbw, etc.
    bowler_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    fielder_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    
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

# Marshmallow Schemas for serialization
class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        include_fk = True

class MatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Match
        include_fk = True

class InningsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Innings
        include_fk = True

class BattingStatsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BattingStats
        include_fk = True

class BowlingStatsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BowlingStats
        include_fk = True

class BallSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ball
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

# Routes for Teams
@app.route('/api/teams', methods=['POST'])
def add_team():
    name = request.json['name']
    logo_url = request.json.get('logo_url')
    
    new_team = Team(name, logo_url)
    db.session.add(new_team)
    db.session.commit()
    
    return team_schema.jsonify(new_team)

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
    
    return player_schema.jsonify(new_player)

@app.route('/api/players', methods=['GET'])
def get_players():
    all_players = Player.query.all()
    return players_schema.jsonify(all_players)

@app.route('/api/players/<id>', methods=['GET'])
def get_player(id):
    player = Player.query.get_or_404(id)
    return player_schema.jsonify(player)

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
    
    return match_schema.jsonify(new_match)

@app.route('/api/matches', methods=['GET'])
def get_matches():
    all_matches = Match.query.all()
    return matches_schema.jsonify(all_matches)

@app.route('/api/matches/<id>', methods=['GET'])
def get_match(id):
    match = Match.query.get_or_404(id)
    return match_schema.jsonify(match)

@app.route('/api/matches/<id>/toss', methods=['PUT'])
def update_toss(id):
    match = Match.query.get_or_404(id)
    
    match.toss_winner = request.json['toss_winner']
    match.toss_decision = request.json['toss_decision']
    match.status = 'in-progress'
    
    db.session.commit()
    return match_schema.jsonify(match)

@app.route('/api/matches/<id>/status', methods=['PUT'])
def update_match_status(id):
    match = Match.query.get_or_404(id)
    
    match.status = request.json['status']
    if request.json['status'] == 'completed':
        match.winner = request.json.get('winner')
    
    db.session.commit()
    return match_schema.jsonify(match)

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
    
    return innings_schema.jsonify(new_innings)

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
    
    return batting_stats_schema.jsonify(new_batting_stats)

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
    
    return bowling_stats_schema.jsonify(new_bowling_stats)

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
    
    return ball_schema.jsonify(new_ball)

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

# Create database tables
with app.app_context():
    db.create_all()
            
if __name__ == '__main__':
    app.run(debug=True)