
class FilePGN:

    def __init__(self, path):
        self.path = path
        self.file = open(path, mode="r")
    
    def get_next_game(self):
        buffer = []
        while True:
            line = self.file.readline().strip()
            if not line:
                continue
            buffer.append(line)
        
            if not line.startswith("["):
                return buffer

    @staticmethod
    def params_to_dict(params):
        params = {
            a: b[1:-1] 
            for a, b in (
                i[1:-1].split(maxsplit=1) 
                for i in params
            )
        }

        new = {}
        str_params = ["Site", "Result", "TimeControl", "Termination"]
        int_params = ["WhiteElo", "BlackElo", "WhiteRatingDiff", "BlackRatingDiff"]
        
        for i in str_params:
            new[i] = params.get(i, "-")
            
        for i in int_params:
            new[i] = int(params[i]) if (i in params) else None

        return new
        
    
    def get_and_parse_next_game(self):
        game = self.get_next_game()
        params = self.params_to_dict(game[:-1])
        
        moves = [
            string
            for string in game[-1].split()
            if string[0].isalpha()
        ]

        moves = [
            self.parse_pgn_move(move, self.get_side(k))
            for k, move in enumerate(moves)
        ]
        
        return (moves, params)

    @staticmethod
    def get_side(k):
        if k % 2 == 0:
            return "w"
        else:
            return "b"

    @staticmethod
    def parse_pgn_move(move, side):
        
        move = move.translate(str.maketrans("", "", "x=+#?!"))

        if (move == "O-O"):
            move = {"w": "Ke1g1", "b": "Ke8g8"}[side]
        if (move == "O-O-O"):
            move = {"w": "Ke1c1", "b": "Ke8c8"}[side]
        
        if move[0].isupper():
            piece, move = move[0], move[1:]
        else:
            piece = "p"

        if move[-1].isupper():
            promotion_to, move = move[-1], move[:-1]
        else:
            promotion_to = ""

        piece = piece.lower()
        promotion_to = promotion_to.lower()
            
        to_square = move[-2:]
        disambig = move[:-2]

        return (side, piece, disambig, to_square, promotion_to)




