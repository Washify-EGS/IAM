import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Keep track of enabled authentication providers
config_file = 'config.json'

def load_config():
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'google': True, 'github': True, 'linkedin': True}

def save_config(config):
    with open(config_file, 'w') as file:
        json.dump(config, file)

enabled_providers = load_config()

@app.route('/')
def index():
    return render_template('index.html', enabled_providers=enabled_providers)

@app.route('/configure', methods=['POST'])
def configure():
    if request.method == 'POST':
        for provider in enabled_providers:
            key = f"{provider}_enabled"
            enabled_providers[provider] = key in request.form

        save_config(enabled_providers)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
