import chess
import chess.engine
from stockfish import Stockfish

STOCKFISH_PATH = "./stockfish-ubuntu-x86-64-vnni512"

class ChessWithStockfish:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.stockfish = Stockfish(stockfish_path)
        self.stockfish.set_skill_level(10)
        self.previous_board = self.get_board_state()  # Save initial state

        
    def display_board(self):
        print(self.board)
    
    def is_game_over(self):
        return self.board.is_game_over()
    
    def get_board_state(self):
        """Returns the current board state as a dictionary of {square: piece}."""
        return {square: self.board.piece_at(square) for square in chess.SQUARES}
    
    def detect_changes(self, previous_state, current_state):
        """Detects changes in the board state between two snapshots."""
        changes = {"emptied": [], "occupied": []}
        for square, piece in previous_state.items():
            current_piece = current_state[square]
            if piece and not current_piece:  # Square was emptied
                changes["emptied"].append(square)
            elif not piece and current_piece:  # Square was occupied
                changes["occupied"].append(square)
        return changes
    
    def detect_move_and_capture(self, previous_state, current_state):
        """Determines the move and detects captures."""
        changes = self.detect_changes(previous_state, current_state)
        if len(changes["emptied"]) == 1 and len(changes["occupied"]) == 1:
            source = changes["emptied"][0]
            destination = changes["occupied"][0]
            capture = current_state[destination] is not None  # Capture if destination is occupied
            return source, destination, capture
        raise ValueError("Unable to detect move or invalid board state!")

    def user_move(self, move):
        try:
            self.board.push_uci(move)
            return True
        except ValueError:
            print("Invalid move! Please try again.")
            return False

    def computer_move(self):
        self.stockfish.set_fen_position(self.board.fen())
        best_move = self.stockfish.get_best_move()
        self.board.push_uci(best_move)
        print(f"Computer moves: {best_move}")
    
    def play_game(self):
        print("ROBOTIC CHESS PLAYING ARM")
        print("Format for moves: 'e2e4' (example: pawn to e4).")
        self.display_board()

        while not self.is_game_over():
            user_move = input("Enter your move: ")
            if self.user_move(user_move):
                self.display_board()
                self.previous_board = self.get_board_state()  # Save board state
                
                if self.is_game_over():
                    break

                print("CPU is thinking...")
                self.computer_move()
                self.display_board()
                current_board = self.get_board_state()
                try:
                    source, destination, capture = self.detect_move_and_capture(self.previous_board, current_board)
                    print(f"Detected move: {chess.square_name(source)} -> {chess.square_name(destination)}")
                    if capture:
                        print(f"Capture detected at {chess.square_name(destination)}")
                except ValueError as e:
                    print(e)
                self.previous_board = current_board  # Update board state

        print("Game Over! Result:", self.get_game_result())


if __name__ == "__main__":
    chess_game = ChessWithStockfish(STOCKFISH_PATH)
    chess_game.play_game()
