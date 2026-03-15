from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing for all routes
CORS(app)

# Data structure to store matches
# Format: matches[match_id] = {"votes": {"Team A": 0, "Team B": 0, "Super Over": 0}, "voted_clients": set()}
matches = {}  # Dictionary to store data for all matches
current_match_id = "match1"  # Default match ID when the server starts

# Initialize the first match with some default votes to show activity
matches[current_match_id] = {
    "votes": {"Team A": 12, "Team B": 8, "Super Over": 5},
    "voted_clients": set()
}

@app.route('/')
def serve_home():
    """Serve the frontend page (index.html)"""
    # This returns the index.html file from the same directory as this script
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route('/vote', methods=['POST'])
def cast_vote():
    # Get the client's IP address from the request
    client_ip = request.remote_addr
    
    # Extract JSON data from the request body
    data = request.get_json()
    
    # Get the user's vote choice from the JSON data
    choice = data.get("choice")
    
    # Get match_id from request or use current_match_id if not specified
    match_id = data.get("match_id", current_match_id)
    
    # If this is a new match we haven't seen before, initialize its data structure
    if match_id not in matches:
        matches[match_id] = {
            "votes": {"Team A": 0, "Team B": 0, "Super Over": 0},  # Initialize vote counters
            "voted_clients": set()  # Initialize empty set to track who voted
        }
    
    # Check if this client already voted in this match
    if client_ip in matches[match_id]["voted_clients"]:
        # If already voted, return an error message with 403 Forbidden status
        return jsonify({"error": "You have already voted in this match!"}), 403
    
    # Check if the vote choice is valid
    if choice in matches[match_id]["votes"]:
        # Increment the vote count for the chosen option
        matches[match_id]["votes"][choice] += 1
        
        # Add the client's IP to the set of clients who have voted in this match
        matches[match_id]["voted_clients"].add(client_ip)
        
        # Return success message and current voting results
        return jsonify({
            "message": "Vote registered!", 
            "votes": calculate_results(match_id)
        })
    else:
        # If invalid choice, return error with 400 Bad Request status
        return jsonify({"error": "Invalid choice!"}), 400

@app.route('/results', methods=['GET'])
def get_results():
    """Return current vote percentages for a match"""
    
    # Get match_id from query parameters or use default
    match_id = request.args.get("match_id", current_match_id)
    
    # Initialize match data if this is a new match ID
    if match_id not in matches:
        matches[match_id] = {
            "votes": {"Team A": 0, "Team B": 0, "Super Over": 0},
            "voted_clients": set()
        }
    
    # Return the voting results for the requested match
    return jsonify({"votes": calculate_results(match_id)})

@app.route('/new-match', methods=['POST'])
def create_new_match():
    """Create a new match with a fresh voting state"""
    
    # Get data from the request
    data = request.get_json()
    
    # Get match_id from request or generate one based on existing matches count
    match_id = data.get("match_id", f"match_{len(matches) + 1}")
    
    # Initialize the new match with empty vote counts and no voted clients
    matches[match_id] = {
        "votes": {"Team A": 0, "Team B": 0, "Super Over": 0},
        "voted_clients": set()
    }
    
    # Update the current default match ID (using global to modify the variable outside the function)
    global current_match_id
    current_match_id = match_id
    
    # Return confirmation message with the new match ID
    return jsonify({
        "message": f"New match created with ID: {match_id}",
        "match_id": match_id
    })

def calculate_results(match_id):
    """Calculate percentage of votes and total vote count for a specific match"""
    
    # If match doesn't exist yet, return zeros for all vote options
    if match_id not in matches:
        return {"Total Votes": 0, "Team A": 0, "Team B": 0, "Super Over": 0}
    
    # Get votes dictionary for this match
    votes = matches[match_id]["votes"]
    
    # Calculate total number of votes cast in this match
    total_votes = sum(votes.values())
    
    # If no votes have been cast yet, return zeros for all percentages
    if total_votes == 0:
        return {"Total Votes": 0, **{option: 0 for option in votes}}
    
    # Calculate percentage for each voting option, rounded to 2 decimal places
    results = {option: round((count / total_votes) * 100, 2) for option, count in votes.items()}
    
    # Add the total vote count to the results
    results["Total Votes"] = total_votes
    
    # Return the complete results dictionary
    return results

# Run the app if this file is executed directly (not imported)
if __name__ == '__main__':
    app.run(debug=True)  # Run in debug mode (auto-reload on code changes)