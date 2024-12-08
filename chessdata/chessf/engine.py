import subprocess
import numpy as np

class ConsoleApp:
    
    def __init__(self, path):
        self.path = path
        self.process = subprocess.Popen(
            path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    
    def write_line(self, line):
        line_bytes = bytes(line, "ascii") + b"\n"
        self.process.stdin.write(line_bytes)
        self.process.stdin.flush()

    def read_line(self):
        line = self.process.stdout.readline()
        line = line.decode("ascii").strip()
        return line

    def skip_lines(self, k):
        for _ in range(k):
            self.process.stdout.readline()





class Position:

    def __init__(self):
        self.fen = None
        self.side_to_move = None
        self.square_to_piece = None
        self.material = None
    
    def update_position(self, fen):
        self.fen = fen
        self.side_to_move = fen.split()[1]
        self.square_to_piece = self.get_square_to_piece(fen)
    
    @staticmethod
    def get_square_to_piece(fen):
        square_id = 0
        square_to_piece = {}
        for char in fen.split()[0]:
            if char.isdigit():
                square_id += int(char)
            elif (char == "/"):
                if square_id % 8 != 0:
                    raise Exception(f"{fen}")
            else:
                file = chr(ord("a") + square_id % 8)
                rank = str(8 - square_id // 8)
                square_to_piece[file+rank] = char
                square_id += 1
        
        if square_id != 64:
            raise Exception(f"{fen}")
        
        return square_to_piece 

    def get_bitboard_matrix(self):
        square_id = 0
        bitboard = np.zeros((12, 64), dtype=np.uint8)

        piece_values = dict(
            K=0, Q=1, R=2, B=3, N=4, P=5,
            k=6, q=7, r=8, b=9, n=10, p=11
        )

        for char in self.fen.split()[0]:
            if char.isdigit():
                square_id += int(char)
            elif (char == "/"):
                if square_id % 8 != 0:
                    raise Exception(f"{fen}")
            else:
                # file = square_id % 8
                # rank = square_id // 8
                piece_layer = piece_values[char]
                bitboard[piece_layer, square_id] = 1
                square_id += 1

        if square_id != 64:
            raise Exception(f"{fen}")

        return bitboard

    def from_long_algebraic(self, move):
        from_square = move[0:2]
        to_square = move[2:4]
        promotion_to = move[4:]
        piece = self.square_to_piece[from_square].lower()
        return (self.side_to_move, piece, from_square, to_square, promotion_to)
    
    def set_pieces(self, moves):
        return [self.from_long_algebraic(move) for move in moves]





class Stockfish(ConsoleApp, Position):

    def __init__(self, path, hash_mb=8, multipv=2):
        super().__init__(path)
        
        self.skip_lines(1)
        self.write_line(f"setoption name Hash value {hash_mb}")
        self.write_line(f"setoption name MultiPV value {multipv}")
        # self.write_line(f"setoption name Threads value 4")
        # self.skip_lines(1)
        self.start_new_game()
    
    def start_new_game(self):
        self.write_line("ucinewgame")
        self.write_line("position startpos")
        self.sync_position()

    def make_alg_move(self, move):
        self.write_line(f"position fen {self.fen} moves {move}")
        self.sync_position()
        
    def sync_position(self):
        self.write_line("d")
        self.skip_lines(20)
        fen = self.read_line()[5:]
        self.update_position(fen)
        self.skip_lines(2)
    
    def get_legal_moves(self):
        self.write_line("go perft 1")
        
        self.skip_lines(4)

        legal_moves = []
        while True:
            line = self.read_line()
            if not line:
                self.skip_lines(2)
                break
            legal_moves.append(line[:-3])

        legal_moves = self.set_pieces(legal_moves)
        
        return legal_moves        

    def get_eval(self, depth):
        self.write_line(f"go depth {depth}")
        self.skip_lines(4)

        best_move = None
        best_eval = None
        second_eval = None

        flip_coeff = (-1) if (self.side_to_move == "b") else 1

        while True:
            line = self.read_line().split()
            if line[0] == "bestmove":
                best_move = line[1]
                break

            d = int(line[2])
        
            if d == depth:
                pv = int(line[6])
                if pv == 1:
                    best_eval = (line[8], int(line[9]) * flip_coeff)
                elif pv == 2:
                    second_eval = (line[8], int(line[9]) * flip_coeff)
                    
            # elif d == 0:
            #     best_eval = (line[4], int(line[5]) * flip_coeff)
            #     second_eval = (line[4], int(line[5]) * flip_coeff)  # forced move

        if second_eval is None:
            second_eval = best_eval
        
        return best_eval, second_eval

    @staticmethod
    def find_compatible(legal_moves, game_move):
        compatible_moves = [
            legal_move for legal_move in legal_moves
            
            if (
                game_move[1] == legal_move[1] and
                game_move[3] == legal_move[3] and
                set(game_move[2]).issubset(set(legal_move[2])) and
                game_move[4] == legal_move[4] and
                game_move[0] == legal_move[0]
            )
        ]
        
        if len(compatible_moves) == 0:
            raise Exception(f"No compatible moves were found")
        if len(compatible_moves) > 1:
            raise Exception(f"More than one compatible move")
        
        return compatible_moves[0]


    def make_pgn_move(self, game_move):
        legal_moves = self.get_legal_moves()        
        made_move = self.find_compatible(legal_moves, game_move)
        made_move_alg = (made_move[2] + made_move[3] + made_move[4])    
        self.make_alg_move(made_move_alg)



