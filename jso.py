import json
import os

# Define the data you want to write to the JSON file
data = {
    "title": "Sample Report",
    "description": "This is a sample description.",
    "items": [
        {"name": "Item 1", "value": 100},
        {"name": "Item 2", "value": 200}
    ]
}

# Define the path where you want to save the JSON file
# For example, saving it in the 'data' directory inside the project
project_directory = os.path.dirname(os.path.abspath(__file__))
json_directory = os.path.join(project_directory, '/Users/amogh1/PycharmProjects/pythonProject/pdfcreate')

# Ensure the 'data' directory exists
os.makedirs(json_directory, exist_ok=True)

# Define the full path for the JSON file
json_file_path = os.path.join(json_directory, 'your_data.json')

# Write the JSON data to the file
try:
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"JSON file has been written to: {json_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
