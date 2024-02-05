import json

def validate_score(score, filename):
    # Construct the path to the JSON file
    json_path = f"/images/{filename}.json"

    try:
        # Read the JSON file
        with open(json_path, 'r') as file:
            data = json.load(file)

        # Extract the score from the JSON data
        json_score = data.get('score')

        # Compare the scores
        if score == json_score:
            return True
        else:
            return False

    except FileNotFoundError:
        return False