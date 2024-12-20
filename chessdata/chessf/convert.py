import numpy as np

# def sigmoid(x, a, b):
#     return 1 / (1 + np.exp((-x+b)/a))

# def eval_to_white_win_p(eval_type, eval_int):
    
#     if eval_type == 'cp':
#         return sigmoid(eval_int, 346.36617387,  67.55444332) 

#     if eval_type == 'mate':
#         return int(eval_int > 0)

#     raise Exception(f"Bad eval: {eval_type} {eval_int}")

# def to_one_hot_bin(win_probability, k=20):
#     eval_bin = np.digitize(win_probability, bins=np.linspace(0, 1, k+1)) - 1
#     return np.eye(k+1)[eval_bin]

def eval_to_white_win_bin(eval_type, eval_int):
    return to_one_hot_bin(eval_to_white_win_p(eval_type, eval_int))

def elo_to_one_hot(elo):
    elo_bin = np.digitize(elo, np.linspace(1200, 2200, 6))
    one_hot = np.zeros(6+1)
    one_hot[elo_bin] = 1
    return one_hot

def elo_diff_to_one_hot(diff):
    diff_bin = np.digitize(diff, bins=[-100, -25, 25, 100]) 
    one_hot = np.zeros(5)
    one_hot[diff_bin] = 1
    return one_hot

def material_diff_to_win_p_bin(diff):
    a = 3.59545593
    win_p = 1 / (1 + np.exp((-diff)/a))
    digit = np.digitize(win_p, bins=np.linspace(0, 1, 11))
    one_hot = np.zeros(11)
    one_hot[digit] = 1
    return one_hot

def move_number_to_one_hot(move_number):
    digit = np.digitize(move_number, [10, 20, 30, 40, 50])
    one_hot = np.zeros(6)
    one_hot[digit] = 1
    return one_hot















    
    