"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    max_score = []
    
    for dice in hand:
        max_score.append(hand.count(dice) * dice)
    
    return max(max_score)
    
    
    
    


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    scores = []
    
    die_sides = [(die + 1) for die in range(num_die_sides)]
    
    pos_outcomes = gen_all_sequences(die_sides, num_free_dice)

    for outcome in pos_outcomes:
        scores.append(score(held_dice + outcome))
        
    expected_result = float(sum(scores))/len(scores)
    
    return expected_result
    
    

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    held_dice = [()]
    
    for dice in hand:
        for dummy_dice in held_dice:
            held_dice = held_dice + [tuple(dummy_dice) + (dice, )]
    

    return set(held_dice)



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    best_hold = (0.0, ())
    current_score = 0
    
    for held_dice in gen_all_holds(hand):
        score = expected_value(held_dice, num_die_sides, len(hand) - len(held_dice))
        if score > current_score:
            current_score = score
            best_hold = (current_score, held_dice)
            
    return best_hold
    

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


import poc_holds_testsuite
poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



