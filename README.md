
# Simon Says Game with Philips Hue Lights

This project implements the classic "Simon Says" game using Philips Hue lights. The game sequence is displayed through the Hue lights, and the player must replicate the sequence by clicking the corresponding buttons on the web interface.

## Features

- Philips Hue light integration to display the game sequence.
- Web interface to start the game and interact with it.
- Visual feedback for button clicks.
- Display the number of steps left in the sequence.
- Restart functionality to reset the game.

## Prerequisites

- Python 3.x
- Philips Hue Bridge and lights
- Flask
- `phue` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/oakljen/simon-says-philips-hue.git
   cd simon-says-philips-hue
   ```

2. Install the required Python packages:
   ```sh
   pip install flask phue
   ```

3. Create a `config.ini` file in the project directory with the following structure:
   ```ini
   [Hue]
   bridge_ip = YOUR_BRIDGE_IP
   group_name = Living Room

   [Game]
   scene_name = Failure Scene

   [Debug]
   print_answer = True
   ```

4. Replace the placeholders in `config.ini` with your actual bridge IP address, group name, and scene name.

## Usage

1. Run the Python script:
   ```sh
   python main.py
   ```

2. The script will open a webpage in your default browser where you can play the "Simon Says" game.

## Game Play

1. Click the "Start Game" button on the web interface to begin the game.
2. Watch the sequence displayed by the Philips Hue lights.
3. Replicate the sequence by clicking the corresponding color buttons on the web interface.
4. The number of steps left in the sequence will be displayed on the screen.
5. If you make a mistake, the lights will flash red, and you can restart the game by clicking the "Restart" button.

## Files

- `main.py`: The main Python script that runs the game.
- `templates/index.html`: The HTML template for the start page.
- `templates/game.html`: The HTML template for the game interface.
- `templates/failure.html`: The HTML template for the failure screen.
- `templates/end.html`: The HTML template for the end screen.
- `config.ini`: Configuration file for the Philips Hue Bridge and game settings.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [phue](https://github.com/studioimaginaire/phue) library for controlling Philips Hue lights with Python.
- [Flask](https://flask.palletsprojects.com/) for providing the web framework.

## Author

- [oakljen](https://github.com/oakljen)
