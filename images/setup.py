import json

def create_json_file(start, end):
    for number in range(start, end + 1):
        # Determine the current turn and dart number within the turn
        turn = ((number - 3) // 3) + 1  # Calculate which turn we're on, starting at 1
        dart_within_turn = (number - 3) % 3 + 1  # Calculate the dart number within the turn
        
        darts = []
        for dart_id in range(turn * 3 - 2, turn * 3 - 2 + dart_within_turn):
            darts.append({"id": dart_id, "score": "0"})
        
        # Create the JSON object
        json_object = {"darts": darts}

        # Write the JSON object to a file
        file_name = f"dart_{number}.json"
        with open(file_name, 'w') as json_file:
            json.dump(json_object, json_file, indent=4)

# Specify the start (3) and end (75) of the range of files to generate
create_json_file(3, 74)
