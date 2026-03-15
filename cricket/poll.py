# Dictionary to store votes
votes = {"Team A": 0, "Team B": 0, "Super Over": 0}

def display_results():
    """Function to display the updated percentage of votes for each option"""
    total_votes = sum(votes.values())
    
    if total_votes == 0:
        print("\nNo votes yet. Start voting!")
        return
    
    print("\nUpdated Poll Results:")
    for option, count in votes.items():
        percentage = (count / total_votes) * 100
        print(f"{option}: {percentage:.2f}% ({count} votes)")

def cast_vote():
    """Function to cast a vote and instantly display results"""
    while True:
        print("\nVote for your favorite option:")
        print("1. Team A")
        print("2. Team B")
        print("3. Super Over")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            votes["Team A"] += 1
        elif choice == "2":
            votes["Team B"] += 1
        elif choice == "3":
            votes["Super Over"] += 1
        else:
            print("Invalid choice, please enter 1, 2, or 3.")
            continue  # Ask again if the input is invalid
        
        display_results()  # Show updated results immediately

# Start the voting process
print("Welcome to the Cricket Poll!")
cast_vote()
