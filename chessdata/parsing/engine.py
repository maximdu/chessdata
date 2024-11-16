import subprocess

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

    def from_long_algebraic(self, move):
        from_square = move[0:2]
        to_square = move[2:4]
        promotion_to = move[4:]
        piece = self.square_to_piece[from_square].lower()
        return (self.side_to_move, piece, from_square, to_square, promotion_to)
    
    def set_pieces(self, moves):
        return [self.from_long_algebraic(move) for move in moves]





class Stockfish(ConsoleApp, Position):

    def __init__(self, path, hash_mb=8):
        super().__init__(path)
        
        self.skip_lines(1)
        self.write_line(f"setoption name Hash value {hash_mb}")
        self.write_line(f"setoption name MultiPV value 2")
        self.start_new_game()
    
    def start_new_game(self):
        self.write_line("ucinewgame")
        self.write_line("position startpos")
        self.sync_position()

    def make_move(self, move):
        self.write_line(f"position fen {self.fen} moves {move}")
        self.sync_position()
        
    def sync_position(self):
        self.write_line("d")

        self.skip_lines(20)
        fen = self.read_line()[5:]
        self.skip_lines(2)
        
        self.update_position(fen)
    
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

    def get_eval(self, depth=20):
        self.write_line(f"go depth {depth}")
        self.skip_lines(4)

        top_moves = {}
        while True:
            line = self.read_line().split()
            if line[0] == "bestmove":
                break

            d = int(line[2])
            if (d == depth) or (d == 0):
                multipv = int(line[6]) if d == depth else 1
                top_moves[multipv] = line
        
            # if d == depth:
            #     multipv = int(line[6])
            #     score_type = line[8]
            #     score_int = int(line[9])
            #     if (self.side_to_move == "b"):
            #         score_int *= -1
            #     if multipv == 1:
            #         best_move = (score_type, score_int)
            #     if multipv == 2:
            #         second_best = (score_type, score_int)
                    
            # elif d == 0:
            #     multipv = 1
            #     score_type = line[4]
            #     score_int = int(line[5])
            #     if (self.side_to_move == "b"):
            #         score_int *= -1
            #     best_move = (score_type, score_int)
            
        
        return top_moves      
