# First, modify the Match model in your models.py or main app file

# Add these fields to your existing Match model class
"""
class Match(db.Model):
    # Existing fields...
    
    # New fields for tournament functionality
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    match_number = db.Column(db.Integer)  # e.g., Match #1, Match #2
    is_knockout = db.Column(db.Boolean, default=False)
    
    # Add relationships
    stage = db.relationship('Stage', foreign_keys=[stage_id], backref='matches')
    group = db.relationship('Group', foreign_keys=[group_id], backref='matches')
"""

# Database migration script to alter the existing tables
# Save this as migrate_db.py and run it to update your database schema

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, Integer, ForeignKey, Boolean

# Initialize Flask app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cricket.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extension
db = SQLAlchemy(app)

def migrate_database():
    with app.app_context():
        # Add new columns to Match table
        try:
            db.engine.execute('ALTER TABLE match ADD COLUMN stage_id INTEGER REFERENCES stage(id)')
            db.engine.execute('ALTER TABLE match ADD COLUMN group_id INTEGER REFERENCES group(id)')
            db.engine.execute('ALTER TABLE match ADD COLUMN match_number INTEGER')
            db.engine.execute('ALTER TABLE match ADD COLUMN is_knockout BOOLEAN DEFAULT 0')
            print("Successfully added tournament columns to Match table")
        except Exception as e:
            print(f"Error adding columns to Match table: {e}")
            # If columns already exist, it's fine
            pass
        
        # Create new tables for tournament features
        try:
            db.engine.execute('''
                CREATE TABLE IF NOT EXISTS tournament (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    start_date DATETIME NOT NULL,
                    end_date DATETIME NOT NULL,
                    description TEXT,
                    logo_url VARCHAR(255),
                    status VARCHAR(20) DEFAULT 'upcoming'
                )
            ''')
            
            db.engine.execute('''
                CREATE TABLE IF NOT EXISTS stage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tournament_id INTEGER NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    sequence INTEGER NOT NULL,
                    stage_type VARCHAR(20) NOT NULL,
                    start_date DATETIME,
                    end_date DATETIME,
                    status VARCHAR(20) DEFAULT 'upcoming',
                    FOREIGN KEY (tournament_id) REFERENCES tournament(id)
                )
            ''')
            
            db.engine.execute('''
                CREATE TABLE IF NOT EXISTS "group" (