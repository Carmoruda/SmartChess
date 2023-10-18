import os
import re
import sys
import serial
import chess
import stockfish
import datetime
import requests

board = chess.Board()

white_player = ""
black_player = ""

ser = serial.Serial('COM5', 9800, timeout=1)

# Telegram bot:
TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


def SendMessage(message):
    """
    Send a message through the telegram bot.
    :param message: Message that wants to be sent.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url).json()


def PieceInSquare(chess_square):
    """
    Identify which piece is placed in a specific square.
    :param chess_square: Coordinate of the box for whose piece we want to check.
    :return: String with the name of the piece.
    """

    piece = board.piece_at(chess.parse_square(chess_square))

    match str(piece).upper():
        case "P":
            return "the pawn"
        case "R":
            return "the rook"
        case "N":
            return "the knight"
        case "B":
            return "the bishop"
        case "Q":
            return "the queen"
        case "K":
            return "the king"


def NewGamePlayerBot():
    """
   Assign one of the players the name entered by the user and the other to stockfish, set stockfish to the starting
   board position and start the game.
   """
    global white_player
    global black_player
    global ser

    clear()
    print(("-" * 30) + " NEW GAME " + ("-" * 30))

    print("   Select one of the following options:\n\t1   Play with white.\n\t2   Play with black.\n")
    menu_action = input("\n  Enter your choice:\n  ===> ")

    clear()
    print(("-" * 30) + " NEW GAME " + ("-" * 30))

    if menu_action == "1":
        white_player = input("\n\t * White player: ")
        black_player = "Stockfish"
        print("\t * Black player: Stockfish")
        input("\n\tPress enter to continue.")
        SendMessage("New game created:\n\t * White player: " + white_player + "\n\t * Black player: " + black_player)

        # Starting position
        stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        clear()
        GamePlayerWhiteBotBlack()
    elif menu_action == "2":
        white_player = "Stockfish"
        print("\n\t * White player: Stockfish")
        black_player = input("\n\t * Black player: ")
        input("\n\tPress enter to continue.")
        SendMessage("New game created:\n\t * WhitePlayer: " + white_player + "\n\t * Black player: " + black_player)

        # Starting position
        stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        clear()
        GamePlayerBlackBotWhite()


def ButtonsInputControl():
    """
    Control the input of the buttons of the square in which the piece is located and the square to which
    it is to be moved, as well as checking if the movement is legal.
    :return: String indicating the player, piece and move made.
    """

    legal_move = False

    button_number = ""
    button_letter = ""

    while not legal_move:
        counter = 0

        # Square in which the piece is located.
        for counter in range(2):
            if counter == 0:
                print("\n\t Enter the letter of the piece's square.")
                button_letter = ButtonInput().split("/")[0]
                print("\t * Letter: " + button_letter + "\n")
            else:
                print("\t Enter the number of the piece's square.")
                button_number = ButtonInput().split("/")[1]
                button_number = int(button_number)
                print("\t * Number: " + str(button_number) + "\n")
            counter += 1

        current_position = (button_letter + str(button_number)).lower()
        piece = PieceInSquare(current_position)

        counter = 0

        # Square to which the piece is to be moved.
        for counter in range(2):
            if counter == 0:
                print("\t Enter the letter of the square you to move to.")
                button_letter = ButtonInput().split("/")[0]
                print("\t * Letter:" + button_letter + "\n")
            else:
                print("\t Enter the number of the square you to move to.")
                button_number = ButtonInput().split("/")[1]
                button_number = int(button_number)
                print("\t * number:" + str(button_number) + "\n")
            counter += 1

        move_position = (button_letter + str(button_number)).lower()

        # Legal move?
        legal_move = chess.Move.from_uci(current_position + move_position) in board.legal_moves

        if legal_move:
            board.push_san(current_position + move_position)

            if not board.turn:  # White turn
                message = ("\tWhite (" + white_player + ") has moved " + piece + " from " + current_position + " to "
                           + move_position + ".")
                SendMessage(message)
            else:  # Black turn
                message = ("\tBlack (" + black_player + ") has moved " + piece + " from " + current_position + " to "
                           + move_position + ".")
                SendMessage(message)

            return message
        else:
            print("\n\t   Error! The movement isn't legal.\n\n")


def ButtonInput():
    """
    Collect the input from the buttons.
    :return: String indicating which button has been pressed.
    """

    for i in range(50):
        line = ser.readline()  # Read a byte.
        if line:
            string = line.decode()  # Convert the byte string to a unicode string.
            # Num = int(string) convert the unicode string to an int
            return string


def NewGamePlayerPlayer():
    """
    Assign black and white players the name entered by the user, set stockfish to the starting
    board position and start the game.
    """
    global white_player
    global black_player
    global ser

    clear()

    print(("-" * 30) + " NEW GAME " + ("-" * 30))
    white_player = input("\n\t* White player: ")
    black_player = input("\n\t* Black player: ")

    input("\n\t Press enter to continue.")

    SendMessage("New game created:\n\t * WhitePlayer: " + white_player + "\n\t * Black player: " + black_player)

    # Starting position
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    Game()


def CheckCheckMate():
    """
    Check current board position to identify is there is a stalemate or checkmate.
    """
    if board.is_checkmate():
        if board.turn:
            print("\nGame over! Black checkmate.\n")
            SendMessage("Game over! Black checkmate")
        else:
            print("\nGame over! White checkmate.\n")
            SendMessage("Game over! White checkmate.")
    elif board.is_stalemate():
        if board.turn:
            print("\nGame over! Stalemate king by Black.\n")
            SendMessage("Game over! Stalemate king by Black.")
        else:
            print("\nGame over! Stalemate king by White.\n")
            SendMessage("Game over! Stalemate king by White.")


def GamePlayerWhiteBotBlack():
    """
    Control of game moves where stockfish is black and the player white.
    """
    counter = 0
    moves = []

    while not board.is_checkmate() and not board.is_stalemate():
        PrintTurn(counter)

        if counter % 2 == 0:
            PlayerMove(moves)

        else:
            StockfishMove(moves)

        SetPositionCheckMate(moves, counter)


def GamePlayerBlackBotWhite():
    """
    Control of game moves where stockfish is white and the player black.
    """
    counter = 0
    moves = []

    while not board.is_checkmate() and not board.is_stalemate():
        PrintTurn(counter)

        if counter % 2 == 0:
            StockfishMove(moves)
        else:
            PlayerMove(moves)

        SetPositionCheckMate(moves, counter)


def SetPositionCheckMate(moves, counter):
    """
    Set stockfish to the new position and check if the there is checkmate/stalemate.
    :param moves: Array of game moves.
    :param counter: Move counter.
    """
    stockfish.set_position(moves)
    print(stockfish.get_board_visual())

    counter += 1

    CheckCheckMate()

    input("\tPress enter to continue.")


def PrintTurn(counter):
    """
    Display the name of the player whose turn it is.
    :param counter: Whose turn it is (even White, odd Black).
    """
    turn = ("-" * 30)

    if counter % 2 == 0:
        turn += white_player.upper() + "'S "
    else:
        turn += black_player.upper() + "'S "

    turn += "TURN"

    clear()
    print(turn + ("-" * 30) + "\n")


def StockfishMove(moves):
    """
    Control stockfish next move and send it through message.
    :param moves: Array of game moves.
    """
    stockfish.set_position(moves)
    next_move = stockfish.get_best_move()
    moves.append(next_move)

    board.push_san(next_move)
    next_move = re.findall('..?', next_move)

    piece = PieceInSquare(next_move[1])

    if not board.turn:
        message = ("\tWhite (" + white_player + ") has moved " + piece + " from " + next_move[0] + " to "
                   + next_move[1] + ".")
    else:
        message = ("\tBlack (" + black_player + ") has moved " + piece + " from " + next_move[0] + " to "
                   + next_move[1] + ".")

    SendMessage(message)
    print("\t" + message + "\n\n")


def PlayerMove(moves):
    """
    Control player next move.
    :param moves: Array of game moves.
    """
    move = ButtonsInputControl()
    print(move + "\n")
    move = move.split()
    moves.append(move[7] + move[9].replace(".", ""))
    PieceInSquare(move[9].replace(".", ""))


def Game():
    """
    Control game logic (whose turn is, if there is checkmate and print board).
    """

    counter = 0

    while not board.is_checkmate() and not board.is_stalemate():
        PrintTurn(counter)
        print(ButtonsInputControl() + "\n")
        print(board)

        CheckCheckMate()

        counter += 1
        input("\tPress enter to continue.")


def NewGameSession():
    """
    Show smart chess name, current date and time.
    """

    clear()
    date_time = datetime.datetime.now()

    welcome_message = ("-" * 50) + " SMART CHESS " + ("-" * 50) + "\n\n"
    welcome_message += "\t * Date: " + date_time.strftime("%d/%m/%Y") + "\n"
    welcome_message += "\t * Time: " + date_time.strftime("%H:%M") + "\n"
    print(welcome_message)


def Menu():
    """
    Menu of the smart chess. User may play games against another player or stockfish.
    :return:
    """

    while True:
        NewGameSession()

        print("   Select one of the following options:\n\t1   New game 1vs1.\n\t2   New game 1vsBot."
              "\n\t3   Exit.")
        menu_option = input("\n  Enter your choice:\n  ===> ")

        match menu_option:
            case "1":
                NewGamePlayerPlayer()
            case "2":
                NewGamePlayerBot()
            case "3":
                sys.exit()
            case _:
                print("\n  Error! The value entered must be 1, 2 or 3.\n")
                input("\tPress enter to continue.")
                clear()


def clear(): os.system('cls')


if __name__ == "__main__":
    stockfish = stockfish.Stockfish(path="stockfish.exe")
    Menu()
