# SmartChess

## Description

SmartChess brings an innovative twist to the traditional game by not only making chess accessible to individuals with visual and other disabilities but also by bridging the physical and digital realms. Our goal is to create a universally accessible, online-capable, autonomous physical chessboard. SmartChess allows players from around the world to engage in real-time chess matches, where moves made on a physical board are reflected in an online environment, and vice versa, enhancing the user experience for all chess enthusiasts.

## Software

The software suite of SmartChess is the core of its operation, enabling online gameplay, autonomous board actions, and inclusive features:

-   `main.py`: The primary Python script orchestrating the gameplay. It communicates with the online environment, processes player inputs, and translates them into physical board movements.
-   `stockfish.exe`: This is the powerhouse behind the chess logic, providing a formidable AI opponent and assisting in game analysis.
-   `bin/speech.mp3`: Audio feedback system that offers an inclusive layer of interaction with the game, facilitating play for users with visual impairments.

Here's an overview of our project structure:

```
SmartChess/
│
├── ArduinoCode/ # Code that interfaces with the physical board
│ └── ChessBoard.ino # Manages LEDs and physical input for an autonomous board
│
├── bin/ # Contains binary files and audio outputs
│ └── speech.mp3 # Stores voice commands and move announcements
│
├── doc/ # Documentation and schematics
│ ├── SmartChess.fzz # Fritzing project file detailing the board's circuit design
│ ├── SmartChess Breadboard.jpg # Actual photo of the breadboard arrangement
│ └── SmartChess Schema.jpg # Visual wiring guide for the board's electronics
│
├── Media/ # Media files related to the project
│ ├── Logo.png # SmartChess logo in PNG for digital use
│ └── Logo.svg # SmartChess logo in SVG for print and high-resolution use
│
├── .gitignore # A list of files and directories to ignore in the repository
├── main.py # The main script enabling the online chess game functionality
└── stockfish.exe # The executable for the Stockfish chess engine
```

## Hardware

SmartChess's hardware design is integral to its mission of inclusivity and online interaction:

-   **Arduino Nano Every**: Empowers the board to operate autonomously, processing in-game actions and user commands.
-   **Custom Breadboard Setup**: Crafted specifically for SmartChess, allowing seamless integration of sensors and actuators that bring the chessboard to life.
-   **LEDs and Display Elements**: Provide clear visual cues for game status and moves, ensuring the game is accessible and engaging.
-   **Responsive Sensors and Actuators**: Translate the online moves to the physical board, allowing for a tactile gaming experience that is rare in online play.

The included documentation, `doc` folder, provides clear instructions and visuals for setting up the hardware. The `SmartChess.fzz` Fritzing file, alongside the breadboard and schematic photos, offers a comprehensive guide for assembling and understanding the interactive chessboard.
