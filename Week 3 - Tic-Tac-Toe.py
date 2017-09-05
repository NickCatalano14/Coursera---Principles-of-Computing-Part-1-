"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 500         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player



# Add your functions here.

def mc_trial(board, player): 
    
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by making random moves, 
    alternating between players. The function should return when the game is over. 
    The modified board will contain the state of the game, so the function does not return anything. 
    In other words, the function should modify the board input.
    """
    
    while (board.check_win() == None):
        move = random.choice(board.get_empty_squares())
        board.move(move[0], move[1], player)
        if (board.check_win() == None):
            player = provided.switch_player(player)
            
    return None

    
def mc_update_scores(scores, board, player): 
     
    """
    This function takes a grid of scores (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a completed game, and which player the 
    machine player is. The function should score the completed board and update the 
    scores grid. As the function updates the scores grid directly, it does not return anything,
    """
    check_winner = board.check_win()
    machine_score = 0
    other_score = 0
    
    if check_winner == player:
        machine_score = SCORE_CURRENT
        other_score = -SCORE_OTHER
    elif check_winner == provided.switch_player(player):
        machine_score = -SCORE_CURRENT
        other_score = SCORE_OTHER      
        
    board_size = board.get_dim()
    
    for dummy_row in range(board_size):
        for dummy_col in range(board_size):
            
            if board.square(dummy_row, dummy_col) == player:
                scores[dummy_row][dummy_col] += machine_score
            elif board.square(dummy_row, dummy_col) == provided.switch_player(player):
                scores[dummy_row][dummy_col] += other_score
        
def get_best_move(board, scores):
    
    """
    This function takes a current board and a grid of scores. The function should find all 
    of the empty squares with the maximum score and randomly return one of them as a 
    (row, column) tuple. It is an error to call this function with a board that has no empty 
    squares (there is no possible next move), so your function may do whatever it wants in 
    that case. The case where the board is full will not be tested.
    """
    available_moves = board.get_empty_squares()
    board_size = board.get_dim()
    best_move = []
    maximum = 0
    
    for dummy_row in range(board_size):
        for dummy_col in range(board_size):
        
            if scores[dummy_row][dummy_col] > maximum and (dummy_row, dummy_col) in available_moves:
                maximum = scores[dummy_row][dummy_col]
                best_move = [(dummy_row,dummy_col)]
            elif scores[dummy_row][dummy_col] == maximum and (dummy_row, dummy_col) in available_moves:
                best_move.append((dummy_row,dummy_col))
            
    return random.choice(best_move)


def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, 
    and the number of trials to run. The function should use the Monte Carlo 
    simulation described above to return a move for the machine player in the 
    form of a (row, column) tuple.
    """
    
    board_size = board.get_dim()
    

    init_scores = [[0 for dummy in range(board_size)] for dummy in range(board_size)]
    
    for dummy in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(init_scores, board_clone, player)
        
    return get_best_move(board, init_scores)




# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
