import chess
import chess.engine
from stockfish import Stockfish
import logging

STOCKFISH_PATH = "./stockfish-ubuntu-x86-64-vnni512"

class ChessWithStockfish:
    def __init__(self, stockfish_path):
        """
        Initialize the Chess game with Stockfish and logging
        
        Args:
            stockfish_path (str): Path to Stockfish executable
        """
        self.board = chess.Board()
        self.stockfish = Stockfish(stockfish_path)
        self.stockfish.set_skill_level(10)
        
        # Setup logging for capture tracking
        logging.basicConfig(level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def display_board(self):
        """Display the current board state"""
        print(self.board)

    def is_game_over(self):
        """Check if the game is over"""
        return self.board.is_game_over()

    def get_game_result(self):
        """
        Determine the specific reason for game over
        
        Returns:
            str: Reason for game termination
        """
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
    
    def detect_capture(self, move):
        """
        Detect if a move is a capture and log details
        
        Args:
            move (str): Move in UCI format
        
        Returns:
            dict: Capture details or None
        """
        try:
            # Convert move to chess.Move
            chess_move = chess.Move.from_uci(move)
            
            # Check if the move is a capture
            if self.board.is_capture(chess_move):
                # Get the captured piece
                captured_piece = self.board.piece_at(chess_move.to_square)
                
                # Prepare capture information
                capture_info = {
                    'is_capture': True,
                    'source_square': chess.square_name(chess_move.from_square),
                    'destination_square': chess.square_name(chess_move.to_square),
                    'captured_piece_type': captured_piece.symbol() if captured_piece else None
                }
                
                # Log capture details
                self.logger.info(f"CAPTURE DETECTED: {capture_info}")
                
                return capture_info
            
            return None
        
        except Exception as e:
            self.logger.error(f"Error detecting capture: {e}")
            return None

    def user_move(self, move):
        """
        Process user's move with capture detection
        
        Args:
            move (str): Move in UCI format
        
        Returns:
            bool: Whether move was successful
        """
        try:
            # Detect capture before pushing the move
            capture_info = self.detect_capture(move)
            
            # Push the move
            self.board.push_uci(move)
            
            # If capture occurred, you can add additional logic here
            # For example, send information to robotic arm
            if capture_info:
                self.handle_capture(capture_info)
            
            return True
        
        except ValueError:
            print("Invalid move! Please try again.")
            return False

    def handle_capture(self, capture_info):
        """
        Handle capture event (placeholder for robotic arm interaction)
        
        Args:
            capture_info (dict): Details of the capture
        """
        print(f"Robotic Arm Capture Event: {capture_info}")
        # Add logic to control robotic arm for piece removal
    
    # def decode(self, grid_map):

    #     pass

    def transition(self):
        grid_map = {
            'h8': [180, 25, 155, 170, 20],
            'h7': [170, 25, 155, 165, 25],
            'h6': [160, 30, 150, 152, 25],
            'h5': [150, 35, 145, 144, 25],
            'h4': [150, 38, 142, 130, 25],
            'h3': [145, 45, 135, 115, 20],
            'h2': [],
            'h1': [],
            'g8': [170, 30, 150, 172, 27],
            'g7': [150, 30, 150, 162, 27],
            'g6': [145, 30, 150, 152, 27],
            'g5': [145, 35, 145, 142, 27],
            'g4': [136, 45, 135, 117, 27],
            'g3': [],
            'g2': [],
            'g1': [],
            'f8': [140, 30, 150, 178, 20],
            'f7': [135, 35, 145, 168, 23],
            'f6': [130, 30, 150, 152, 23],
            'f5': [128, 32, 148, 144, 20],
            'f4': [128, 38, 142, 130, 20],
            'f3': [123, 42, 138, 120, 20],
            'f2': [],
            'f1': [],
            'e8': [125, 30, 150, 178, 20],
            'e7': [120, 35, 145, 168, 23],
            'e6': [118, 30, 150, 152, 20],
            'e5': [118, 32, 148, 144, 20],
            'e4': [115, 38, 142, 130, 25],
            'e3': [115, 42, 138, 120, 25],
            'e2': [],
            'e1': [],
            'd8': [],
            'd7': [],
            'd6': [],
            'd5': [],
            'd4': [],
            'd3': [],
            'd2': [],
            'd1': [],
            'c8': [],
            'c7': [],
            'c6': [],
            'c5': [],
            'c4': [],
            'c3': [],
            'c2': [],
            'c1': [],
            'b8': [],
            'b7': [],
            'b6': [],
            'b5': [],
            'b4': [],
            'b3': [],
            'b2': [],
            'b1': [],
            'a8': [],
            'a7': [],
            'a6': [],
            'a5': [],
            'a4': [],
            'a3': [],
            'a2': [],
            'a1': []
        }

    



    def computer_move(self):
        """
        Generate and process computer's move with capture detection
        """
        self.stockfish.set_fen_position(self.board.fen())
        best_move = self.stockfish.get_best_move()
        
        # Detect capture for computer's move
        capture_info = self.detect_capture(best_move)
        
        # Push the move
        self.board.push_uci(best_move)

        # cpu_move = best_move


        
        print(f"Computer moves: {best_move}")
        
        # If capture occurred, handle it
        if capture_info:
            self.handle_capture(capture_info)
    
    def play_game(self):
        """
        Main game loop with enhanced move tracking
        """
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