
# Move is just a tuple instead of a separate class for 2 reasons:
# 1) Tuples are faster since it is just get-by-index, not get-by-name 
# 2) Tuples are frozen (dataclasses can be too but slower to create)
    
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

def to_long_algebraic(move):
    return move[2] + move[3] + move[4]










