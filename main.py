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
    Sends a message through the telegram bot.
    :param message: Message that wants to be sent.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url).json()


def PieceInSquare(chess_square):
    piece = board.piece_at(chess.parse_square(chess_square))

    if str(piece).upper() == "P":
        return "the pawn"
    elif str(piece).upper() == "R":
        return "the rook"
    elif str(piece).upper() == "N":
        return "the knight"
    elif str(piece).upper() == "B":
        return "the bishop"
    elif str(piece).upper() == "Q":
        return "the queen"
    elif str(piece).upper() == "K":
        return "the king"


def ButtonsInputControl():
    legal_move = False

    button_number = ""
    button_letter = ""

    while not legal_move:
        counter = 0

        # Square of the piece the user wants to move.
        for counter in range(2):
            if counter == 0:
                print("\n\t Enter the letter of the piece's square.")
                button_letter = ButtonInput().split("/")[0]
                print("\t * Letter:" + button_letter + "\n")
            else:
                print("\t Enter the number of the piece's square.")
                button_number = ButtonInput().split("/")[1]
                button_number = int(button_number)
                print("\t * Number:" + str(button_number) + "\n")
            counter += 1

        current_position = (button_letter + str(button_number)).lower()
        piece = PieceInSquare(current_position)

        counter = 0

        # Square the user wants to move the piece to.
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

        legal_move = chess.Move.from_uci(current_position + move_position) in board.legal_moves

        if legal_move:
            board.push_san(current_position + move_position)

            if not board.turn:
                message = ("\tWhite (" + white_player + ") has moved " + piece + " from " + current_position + " to "
                           + move_position + ".")
                SendMessage(message)
            else:
                message = ("\tBlack (" + black_player + ") has moved " + piece + " from " + current_position + " to "
                           + move_position + ".")
                SendMessage(message)

            return message
        else:
            print("\n\t   Error! The movement isn't legal.\n\n")


def ButtonInput():
    for i in range(50):
        line = ser.readline()  # Read a byte.
        if line:
            string = line.decode()  # Convert the byte string to a unicode string.
            # Num = int(string) convert the unicode string to an int
            return string


def NewGamePlayerPlayer():
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


def NewGamePlayerBot():
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
        print("\n\t * Black player: Stockfish")
        input("\n\tPress enter to continue.")
        SendMessage("New game created:\n\t * WhitePlayer: " + white_player + "\n\t * Black player: " + black_player)

        # Starting position
        stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        clear()
        GamePlayerWhiteBotBack()
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


def CheckCheckMate():
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


def GamePlayerWhiteBotBack():
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

    stockfish.set_position(moves)
    print(stockfish.get_board_visual())

    counter += 1

    CheckCheckMate()

    input("\tPress enter to continue.")


def PrintTurn(counter):
    turn = ("-" * 30)

    if counter % 2 == 0:
        turn += white_player.upper() + "'S "
    else:
        turn += black_player.upper() + "'S "

    turn += "TURN"

    clear()
    print(turn + ("-" * 30) + "\n")


def StockfishMove(moves):
    stockfish.set_position(moves)
    next_move = stockfish.get_best_move()
    moves.append(next_move)

    board.push_san(next_move)
    next_move = re.findall('..?', next_move)

    piece = PieceInSquare(next_move[1])

    if not board.turn:
        message = ("\tBlack (" + black_player + ") has moved " + piece + " from " + next_move[0] + " to "
                   + next_move[1] + ".")
    else:
        message = ("\tBlack (" + black_player + ") has moved " + piece + " from " + next_move[0] + " to "
                   + next_move[1] + ".")

    SendMessage(message)
    print("\t" + message + "\n\n")


def PlayerMove(moves):
    move = ButtonsInputControl()
    print(move + "\n")
    move = move.split()
    moves.append(move[7] + move[9].replace(".", ""))
    PieceInSquare(move[9].replace(".", ""))


def Game():
    counter = 0

    while not board.is_checkmate() and not board.is_stalemate():
        PrintTurn(counter)
        print(ButtonsInputControl() + "\n")
        print(board)

        CheckCheckMate()

        counter += 1
        input("\tPress enter to continue.")


def NewGameSession():
    clear()
    date_time = datetime.datetime.now()

    welcome_message = ("-" * 50) + " SMART CHESS " + ("-" * 50) + "\n\n"
    welcome_message += "\t * Día: " + date_time.strftime("%d/%m/%Y") + "\n"
    welcome_message += "\t * Hora: " + date_time.strftime("%H:%M") + "\n"
    print(welcome_message)


def Menu():

    while True:
        NewGameSession()

        print("   Select one of the following options:\n\t1   New game 1vs1.\n\t2   New game 1vsBot."
              "\n\t3   Exit.")
        menu_option = input("\n  Enter your choice:\n  ===> ")

        if menu_option == "1":
            NewGamePlayerPlayer()
        elif menu_option == "2":
            NewGamePlayerBot()
        elif menu_option == "3":
            sys.exit()
        else:
            print("\n  Error! The value entered must be 1, 2 or 3.\n")
            input("\tPress enter to continue.")
            clear()


def clear(): os.system('cls')


if __name__ == "__main__":
    stockfish = stockfish.Stockfish(path="stockfish.exe")
    Menu()
