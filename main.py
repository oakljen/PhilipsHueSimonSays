import configparser
import time
from phue import Bridge
import random
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

bridge_ip = config['Hue']['bridge_ip']
group_name = config['Hue']['group_name']
scene_name = config['Game']['scene_name']
print_answer = config['Debug'].getboolean('print_answer')

# Connect to the bridge
b = Bridge(bridge_ip)

# Define colors in XY format for Philips Hue
colors = {
    "Red": [0.675, 0.322],
    "Green": [0.4091, 0.818],
    "Blue": [0.167, 0.04],
    "Yellow": [0.432, 0.500]
}

# Get the group lights
group_lights = b.get_group(group_name)['lights']
lights = {b.get_light(int(light_id), 'name'): b.get_light_objects('id')[int(light_id)] for light_id in group_lights}

# Select 4 random lights
selected_lights = random.sample(list(lights.keys()), 4)

# Initialize game sequence
sequence = []

# Assign colors to selected lights and set them dim initially
light_color_map = {}
for i, light in enumerate(selected_lights):
    color_name = list(colors.keys())[i % len(colors)]
    light_color_map[light] = color_name
    lights[light].xy = colors[color_name]
    lights[light].brightness = 100  # Set brightness to dim but not too dim

# Function to change the brightness of a light with a faster transition time
def change_light_brightness(light, brightness, transition_time=1):
    b.set_light(lights[light].light_id, 'transitiontime', transition_time)
    lights[light].brightness = brightness

# Function to flash all lights red
def flash_failure():
    for light in selected_lights:
        lights[light].xy = colors["Red"]
        change_light_brightness(light, 254, 1)

# Function to trigger a Philips Hue scene
def trigger_scene(scene_name):
    b.run_scene(group_name, scene_name)

# Function to reset lights to dim
def reset_lights_to_dim():
    for light in selected_lights:
        change_light_brightness(light, 100)

# Function to play the sequence
def play_sequence():
    for light in sequence:
        change_light_brightness(light, 254, 1)
        time.sleep(0.5)  # Stay on for 500 milliseconds
        change_light_brightness(light, 100, 10)
        time.sleep(0.5)  # Wait for the transition to complete

# Flask app to display the webpage
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game')
def start_game():
    sequence.clear()
    next_light = random.choice(selected_lights)
    sequence.append(next_light)
    play_sequence()
    if print_answer:
        sequence_colors = [light_color_map[light] for light in sequence]
        print(f"Initial sequence: {sequence_colors}")
    return redirect(url_for('game'))

@app.route('/game')
def game():
    step = request.args.get('step', 0, type=int)
    total_steps = len(sequence)
    steps_left = total_steps - step
    return render_template('game.html', step=step, steps_left=steps_left)

@app.route('/new_step')
def new_step():
    next_light = random.choice(selected_lights)
    sequence.append(next_light)
    play_sequence()
    if print_answer:
        sequence_colors = [light_color_map[light] for light in sequence]
        print(f"Current sequence: {sequence_colors}")
    return redirect(url_for('game'))

@app.route('/select_color', methods=['POST'])
def select_color():
    selected_color = request.form['color']
    current_step = int(request.form['step'])
    correct_light = sequence[current_step]
    correct_color = light_color_map[correct_light]
    
    if selected_color == correct_color:
        if current_step + 1 == len(sequence):
            reset_lights_to_dim()  # Reset lights to dim after correct sequence
            return redirect(url_for('new_step'))
        else:
            return redirect(url_for('game', step=current_step + 1))
    else:
        flash_failure()
        trigger_scene(scene_name)
        return render_template('failure.html')

@app.route('/end_game')
def end_game():
    reset_lights_to_dim()
    return render_template('end.html')

@app.route('/restart_game')
def restart_game():
    reset_lights_to_dim()
    return redirect(url_for('start_game'))

if __name__ == '__main__':
    # Open the web browser after a slight delay to ensure the Flask app is running
    def open_browser():
        webbrowser.open('http://localhost:5000')
    
    from threading import Timer
    Timer(1, open_browser).start()
    
    # Run the Flask app
    app.run(debug=True)
