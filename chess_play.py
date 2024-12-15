import chess
import chess.engine
from stockfish import Stockfish

STOCKFISH_PATH = "./stockfish-ubuntu-x86-64-vnni512"

class ChessWithStockfish:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.stockfish = Stockfish(stockfish_path)
        self.stockfish.set_skill_level(10)
    
    def display_board(self):
        print(self.board)

    def is_game_over(self):
        return self.board.is_game_over()

    def get_game_result(self):
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Insufficient material"
        elif self.board.is_seventyfive_moves():
            return "75-move rule"
        elif self.board.is_fivefold_repetition():
            return "Fivefold repetition"
        else:
            return "Game Over"
    
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
                if self.is_game_over():
                    break

                print("CPU is thinking...")
                self.computer_move()
                self.display_board()

        print("Game Over! Result:", self.get_game_result())


if __name__ == "__main__":
    chess_game = ChessWithStockfish(STOCKFISH_PATH)
    chess_game.play_game()
