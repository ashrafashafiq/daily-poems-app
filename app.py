import os
import random
import yaml
from flask import Flask, jsonify, render_template

# Initialize Flask app
app = Flask(__name__)

# Path to the folder where your poems are stored
POEMS_DIR = os.path.join(os.getcwd(), 'data', 'poems')

def load_random_poem():
    # Traverse all subfolders in the poems directory to get all poem files
    poem_files = []
    for root, dirs, files in os.walk(POEMS_DIR):
        for file in files:
            if file.endswith('.yaml'):
                poem_files.append(os.path.join(root, file))
    
    # Select a random poem file
    random_poem_file = random.choice(poem_files)

    # Load the selected poem from the YAML file
    with open(random_poem_file, 'r', encoding='utf-8') as f:
        poem_data = yaml.safe_load(f)

    # Extract Urdu and English versions of the poem
    poem_title = {entry['lang']: entry['text'] for entry in poem_data['heading']}
    poem_body = [{'ur': sher['sherContent'][0]['text'], 'en': sher['sherContent'][1]['text']} for sher in poem_data['sher']]

    return poem_title, poem_body

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/random_poem', methods=['GET'])
def random_poem():
    poem_title, poem_body = load_random_poem()
    return jsonify({
        'title_ur': poem_title.get('ur', ''),
        'title_en': poem_title.get('en', ''),
        'poem_body': poem_body
    })

if __name__ == '__main__':
    app.run(debug=True)
