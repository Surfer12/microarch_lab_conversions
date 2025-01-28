import argparse
import sys

# Import your existing classes
from educational.learning_pathways import (
    LearningState,
    AdaptiveLearningPathway,
    DifficultyLevel
)

def main():
    parser = argparse.ArgumentParser(
        description="CLI for the Adaptive Learning Pathway"
    )
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command',
        help='Available commands'
    )

    # -----------------------------
    # Command: start
    # -----------------------------
    start_parser = subparsers.add_parser(
        'start',
        help='Start a new learning session'
    )
    # Optional arguments can be added here, if needed

    # -----------------------------
    # Command: submit
    # -----------------------------
    submit_parser = subparsers.add_parser(
        'submit',
        help='Submit challenge results'
    )
    submit_parser.add_argument(
        '--solving-time',
        type=int,
        required=True,
        help='Solving time in seconds'
    )
    submit_parser.add_argument(
        '--error-rate',
        type=float,
        required=True,
        help='Difficulty level for the challenge (e.g., beginner, intermediate, advanced, expert)'
    )
    submit_parser.add_argument(
        '--challenge-level',
        type=str,
        required=True,
        help='Difficulty level for the challenge (e.g., beginner, intermediate, advanced, expert)'
    )

    # -----------------------------
    # Command: state
    # -----------------------------
    state_parser = subparsers.add_parser(
        'state',
        help='View the current learning state'
    )

    args = parser.parse_args()

    # Initialize learning state
    learning_state = LearningState()
    learning_pathway = AdaptiveLearningPathway(initial_state=learning_state)

    # -----------------------------
    # Route command logic
    # -----------------------------
    if args.command == 'start':
        print("\n=== Starting a new learning session ===")
        # Optionally, set initial difficulty here
        print(f"Current difficulty set to: {learning_state.difficulty_level.name}")

    elif args.command == 'submit':
        # Validate the user-supplied difficulty level
        try:
            challenge_enum = DifficultyLevel[args.challenge_level.upper()]
        except KeyError:
            valid_levels = [level.name.lower() for level in DifficultyLevel]
            print(f"Error: Invalid challenge level '{args.challenge_level}'.")
            print(f"Must be one of: {valid_levels}")
            return

        # Create a challenge result
        result = {
            'solving_time': args.solving_time,
            'error_rate': args.error_rate,
            'challenge': challenge_enum
        }

        # Submit the challenge result
        learning_pathway.submit_challenge_result(result)
        print("\n=== Challenge result submitted ===")
        print(f"  Time: {args.solving_time} seconds")
        print(f"  Error Rate: {args.error_rate}")
        print(f"  Challenge Level: {challenge_enum.name}")
        print(f"New difficulty level: {learning_state.difficulty_level.name}")

    elif args.command == 'state':
        print("\n=== Current Learning State ===")
        print(f"Difficulty Level        : {learning_state.difficulty_level.name}")
        print(f"Completed Challenges    : {len(learning_state.completed_challenges)}")
        # Add more details as needed

    else:
        # If no valid command is provided
        parser.print_help()

def load_learning_state():
    import json
    import os
    STATE_FILE = 'learning_state.json'

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state_data = json.load(f)
            return LearningState.from_dict(state_data)
    else:
        return LearningState()

def save_learning_state(state):
    import json
    STATE_FILE = 'learning_state.json'
    with open(STATE_FILE, 'w') as f:
        json.dump(state.to_dict(), f)

if __name__ == "__main__":
    main()