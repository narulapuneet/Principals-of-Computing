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
    scores=[0]*max(hand)
    for num in xrange(1,max(hand)+1):
        for die in hand:
            if die == num:
                scores[num-1]+=num
    return max(scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes=gen_all_sequences(xrange(1,num_die_sides+1),num_free_dice)
    score_sum=0.0
    for outcome in outcomes:
        score_sum+=score(held_dice+outcome)
    return score_sum/len(outcomes)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = set([()])
    for die in hand:
        temp = set()
        for partial_hold in holds:
            temp.add(partial_hold)
            new_hold=list(partial_hold)
            new_hold.append(die)
            temp.add(tuple(new_hold))
        holds = temp
    return holds

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_value=0
    result=[]
    for hold in gen_all_holds(hand):
        if expected_value(hold,num_die_sides,len(hand)-len(hold)) > max_value:
            max_value=expected_value(hold,num_die_sides,len(hand)-len(hold))
            result=[expected_value(hold,num_die_sides,len(hand)-len(hold)),hold]
    return tuple(result)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (6,6,3)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
   
    


