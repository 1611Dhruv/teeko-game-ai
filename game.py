import random
import time
import tkinter as tk
from tkinter import messagebox

MAX_DEPTH = 3


class TeekoPlayer:
    """An object representation for an AI game player for the game Teeko."""

    board = [[" " for j in range(5)] for i in range(5)]
    pieces = ["b", "r"]

    def __init__(self):
        """Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.pieceCount = 0

    def make_move(self, state):
        """Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        val, move = self.minimax(state, 0, True, self.pieceCount, None)
        # ensure the destination (row,col) tuple is at the beginning of the move list
        self.board[move[0][0]][move[0][1]] = self.my_piece
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = " "
            self.pieceCount -= 1
        self.pieceCount += 1
        self.print_board()
        print(self.pieceCount)
        return move

    def minimax(self, state, depth, aiTurn, pieceCount, prevMove) -> tuple:
        """
        The minimax function. Takes in the current state, depth, whether or not it is AI's turn
        pieceCount, and the previously made move

        Outputs the best possible value our agent can make along with his best move
        """
        # Base case: If we surpass max Depth or value is non zero return
        val = self.game_value(state)
        if depth > MAX_DEPTH or val != 0:
            return val, prevMove

        myPiece = self.my_piece if aiTurn else "b" if self.my_piece == "r" else "r"
        minOrMaxWant = 1 if aiTurn else -1

        defaultMove = None
        defaultVal = None

        if pieceCount < 8:

            for i in range(5):
                for j in range(5):
                    if state[i][j] == " ":
                        move = [(i, j)]
                        state[i][j] = myPiece
                        f_v, bestFutureMove = self.minimax(
                            state, depth + 1, not aiTurn, pieceCount + 1, move
                        )
                        state[i][j] = " "
                        if f_v == minOrMaxWant:
                            return f_v, move
                        if f_v == 0 or defaultMove == None:
                            defaultMove = move
                            defaultVal = f_v

        else:
            myPiecesLoc = [
                (i, j) for i in range(5) for j in range(5) if state[i][j] == myPiece
            ]

            for loc in myPiecesLoc:
                for k in range(9):
                    if k == 4:
                        continue
                    changes = (k // 3 - 1, k % 3 - 1)
                    new_ij = (loc[0] - changes[0], loc[1] - changes[1])
                    # if our actions are infeasible, continue
                    if (
                        new_ij[0] < 0
                        or new_ij[1] < 0
                        or new_ij[0] > 4
                        or new_ij[1] > 4
                        or state[new_ij[0]][new_ij[1]] != " "
                    ):
                        continue
                    move = [new_ij, loc]
                    state[new_ij[0]][new_ij[1]] = myPiece
                    state[loc[0]][loc[1]] = " "
                    f_v, bestFutureMove = self.minimax(
                        state, depth + 1, not aiTurn, pieceCount, move
                    )
                    state[loc[0]][loc[1]] = myPiece
                    state[new_ij[0]][new_ij[1]] = " "
                    if f_v == minOrMaxWant:
                        return f_v, move
                    if f_v == 0 or defaultMove == None:
                        defaultMove = move
                        defaultVal = f_v

        return defaultVal, defaultMove

    def opponent_move(self, move):
        """Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception("Illegal move: Can only move to an adjacent space")
        if self.board[move[0][0]][move[0][1]] != " ":
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = " "
            self.pieceCount -= 1
        self.board[move[0][0]][move[0][1]] = piece
        self.pieceCount += 1

    def print_board(self):
        """Formatted printing for the board"""
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != " " and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if (
                    state[i][col] != " "
                    and state[i][col]
                    == state[i + 1][col]
                    == state[i + 2][col]
                    == state[i + 3][col]
                ):
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        win = state[0][0]
        for i in range(5):
            if win == " ":
                win = None
                break
            if win != state[i][i]:
                win = None
        if win != None:
            return 1 if win == self.my_piece else -1

        win = state[0][4]
        for i in range(5):
            if win == " ":
                win = None
                break
            if win != state[i][4 - i]:
                win = None

        # TODO: check / diagonal wins
        if win != None:
            return 1 if win == self.my_piece else -1

        # TODO: check box wins
        for i in range(4):
            for j in range(4):
                if (
                    state[i][j] != " "
                    and state[i][j]
                    == state[i + 1][j]
                    == state[i][j + 1]
                    == state[i + 1][j + 1]
                ):
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################


MAX_DEPTH = 3


class TeekoGUI:
    """
    GUI class for the Teeko game.

    Attributes:
        master (tk.Tk): The root Tkinter window.
        board (list of lists): Represents the game board with empty spaces initially.
        pieces (list): List of piece colors ('b' for black, 'r' for red).
        ai (TeekoPlayer): Instance of TeekoPlayer for AI moves.
        buttons (list of lists): 2D list of Tkinter Buttons representing the game board.
        selected_button (tuple): Stores the coordinates (row, col) of the selected button.
        phase (str): Current game phase ('drop' or 'move').
    """

    def __init__(self, master):
        """
        Initializes the TeekoGUI.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        self.master.title("Teeko Game")
        self.board = [[" " for j in range(5)] for i in range(5)]
        self.pieces = ["b", "r"]
        self.ai = TeekoPlayer()
        self.phase = "drop"  # Initial phase is 'drop'
        self.selected_button = None  # No button initially selected

        self.buttons = []
        for i in range(5):
            buttons = []
            for j in range(5):
                buttons.append(
                    tk.Button(
                        self.master,
                        text=" ",
                        width=5,
                        height=2,
                        command=lambda row=i, col=j: self.handle_click(row, col),
                    )
                )
                buttons[j].grid(row=i, column=j)
            self.buttons.append(buttons)

        if self.ai.my_piece == "b":
            self.ai_move()

    def handle_click(self, row, col):
        """
        Handles button clicks based on the current game phase.

        Args:
            row (int): Row index of the clicked button.
            col (int): Column index of the clicked button.
        """
        move = []
        if self.phase == "drop":
            # Handle piece placement during the 'drop' phase
            if self.board[row][col] == " ":
                move = [(row, col)]
        elif self.phase == "move":
            # Handle piece movement during the 'move' phase
            if self.selected_button is None:
                # Selecting the piece to move
                if self.board[row][col] == self.ai.opp:
                    self.selected_button = (row, col)
                    self.buttons[row][col].config(bg="blue")  # Highlight selected piece
                    self.update_buttons()
                    print(f"Selected piece at {row}, {col}")

            else:
                # Moving the selected piece to an empty space
                if self.board[row][col] == " ":
                    move = [(row, col), self.selected_button]
                    print(move)
        try:
            if move:
                self.ai.opponent_move(move)
                self.place_piece(move, self.ai.opp)
                if self.ai.pieceCount >= 7:
                    self.phase = "move"  # Switch to 'move' phase after placing 8 pieces
                self.selected_button = None  # Reset selected button after move
                self.ai_move()
        except Exception as e:
            print(e)
            self.selected_button = None  # Reset selected button after movea
            self.update_buttons()

    def ai_move(self):
        """
        AI makes a move on the game board.
        """
        move = self.ai.make_move(self.board)
        self.place_piece(move, self.ai.my_piece)

    def place_piece(self, move, piece):
        """
        Places a piece on the game board and updates the GUI buttons.

        Args:
            move (list): List of move tuples. [(row, col), (source_row, source_col)] if moving piece, else [(row, col)].
            piece (str): Piece color ('b' or 'r') to place on the board.
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = " "
        self.board[move[0][0]][move[0][1]] = piece
        self.update_buttons()

        # Check game state after placing the piece
        if self.game_value() == 1:
            messagebox.showinfo("Game Over", "AI wins!")
        elif self.game_value() == -1:
            messagebox.showinfo("Game Over", "Player wins!")

    def game_value(self):
        """
        Checks the current game board for a win condition.

        Returns:
            int: 1 if AI wins, -1 if player wins, 0 if no winner yet.
        """
        return self.ai.game_value(self.board)

    def reset_board(self):
        """
        Resets the game board and updates the GUI buttons.
        """
        self.board = [[" " for j in range(5)] for i in range(5)]
        self.phase = "drop"  # Reset to 'drop' phase
        self.selected_button = None  # Reset selected button
        self.ai = TeekoPlayer()
        self.update_buttons()

    def update_buttons(self):
        """
        Updates the text and color of GUI buttons based on the current state of the game board.
        """
        for i in range(5):
            for j in range(5):
                piece = self.board[i][j]
                if piece == "b":
                    if self.selected_button == (i, j):
                        self.buttons[i][j].config(text="<b>", bg="black")
                    else:
                        self.buttons[i][j].config(text="b", bg="blue")
                elif piece == "r":
                    if self.selected_button == (i, j):
                        self.buttons[i][j].config(text="<r>", bg="red")
                    else:
                        self.buttons[i][j].config(text="r", bg="blue")
                else:
                    self.buttons[i][j].config(
                        text=" ", bg="SystemButtonFace"
                    )  # Default color


def main():
    root = tk.Tk()
    teeko_gui = TeekoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
