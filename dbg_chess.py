import chess
from stockfish import Stockfish


board = chess.Board()
# print(board)

stockfish = Stockfish("./stockfish-ubuntu-x86-64-vnni512")

stockfish.set_depth(20)
stockfish.set_skill_level(10)
stockfish.get_parameters()

print(stockfish.get_best_move())