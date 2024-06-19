# Teeko Game Application

## Overview

This is a graphical user interface (GUI) implementation of the Teeko game using Python's Tkinter library with ttk styles. Teeko is a two-player strategy board game.

![Teeko Game Screenshot](teeko_game_screenshot.png)

## Features

- Allows players to place pieces on a 5x5 board.
- Supports two phases:
  - **Drop Phase**: Players place their pieces until they have placed 8 pieces.
  - **Move Phase**: Players can move their pieces to adjacent empty spaces.
- AI opponent included for single-player mode.
- Game state and moves are displayed graphically using GUI buttons.

## Installation

To run the Teeko game application, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your/repository.git
   cd repository-directory
   ```

2. Install dependencies (assuming you have Python and pip installed):

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python teeko_gui.py
   ```

## Usage

- **Game Rules**: Teeko is played on a 5x5 board. Players alternate turns placing pieces ('b' for black and 'r' for red) until each has placed 8 pieces. In the Move Phase, players can move their pieces to an adjacent empty space.
- **Interface**: Buttons represent spaces on the board. Clicking a button places or moves a piece depending on the game phase.

## Technologies Used

- Python 3
- Tkinter for GUI development
- ttk styles for enhanced widget styling

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/add-new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/add-new-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
