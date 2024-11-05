# PygameCrawler2

PygameCrawler2 is a 2D top-down game developed using Python's Pygame library. The player navigates through levels, interacts with objects, and battles enemies, all while being kept centered on the screen. The game features dynamic player health, mana, and stamina bars, as well as AI-driven enemies with different behavior states.

## Features
- **Player Movement**: The player can move in four directions using WASD keys.
- **Attack Direction Indicator**: A visual guide that shows where the player is aiming.
- **Enemies**: AI-driven enemies with wandering, patrolling, and chasing behaviors.
- **Map System**: The level is generated from a JSON map file, with various tile types like floors, walls, and doors.
- **Doors**: Players can interact with doors, which expand and change as players approach.
- **Status Bars**: Health, mana, and stamina are displayed on the screen to indicate the player's current stats.

## Getting Started
### Prerequisites
- Python 3.7 or higher
- Pygame library

### Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/Clivej13/PygameCrawler2.git
   ```
2. Install the required Pygame library:
   ```sh
   pip install pygame
   ```

### Running the Game
1. Run the `main.py` script to start the game:
   ```sh
   python main.py
   ```
2. Use the WASD keys to move the player and the mouse to aim.

## File Structure
- **main.py**: Contains the main game loop, handles initialization, input, and rendering.
- **map.py**: Loads the level map and manages tiles, enemies, doors, and the player.
- **player.py**: Defines the player's properties, movement, interaction with doors, and health/mana/stamina management.
- **enemy.py**: Handles enemy behaviors including wandering, patrolling, and chasing.
- **door.py, wall.py, floor.py**: Define the static objects that make up the game environment.
- **attack_direction_indicator.py**: Displays where the player is aiming.
- **status_bars.py**: Manages the visual status bars for health, mana, stamina, and XP.
- **sprite.py**: Base classes for different sprite types used in the game.

## Controls
- **Movement**: `WASD` keys
- **Interact with Doors**: `Q` key
- **Aim**: Move the mouse

## Future Improvements
- Adding new enemy types with different AI behaviors.
- Implementing additional levels with unique layouts.
- Adding more player abilities or items.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request if you'd like to add features or fix bugs.

## License
This project is open-source and available under the MIT License.

