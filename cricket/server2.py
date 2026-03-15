from flask import Flask,request, jsonify, send_from_directory
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)


votes = {"Team A": 0, "Team B": 0, "Super Over": 0}

@app.route('/')
def home():
    return send_from_directory(os.path.dirname(__file__),'index.html')


@app.route('/vote', methods=['POST']) 
def cast_vote():
    data = request.get_json()
    choice = data.get("choice")

    if choice in votes:
        votes[choice] += 1
        return jsonify({"message": "Vote registered!", "votes": calculate_results()})
    else:
        return jsonify({"error": "Invalid choice!"}), 400
    


@app.route('/results', methods=['GET'])
def get_results():
    return jsonify({"votes": calculate_results()})

def calculate_results():
    total_votes = sum(votes.values())
    if total_votes == 0:
        return{"Total Votes":0,**{option:0 for option in votes}}
    
    results= {option:round((count/total_votes)*100,2) for option,count in votes.items()}
    results["Total Votes"] = total_votes
    return results


if __name__ == '__main__':
    app.run(debug=True)


    



