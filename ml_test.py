import pandas as pd
import random
import time

start = time.time()


def compute_score(rem):
    if int(rem) < 10:
        score = 9
    elif int(rem) > 10 and int(rem) < 100:
        score = 8
    elif int(rem) > 100 and int(rem) < 1000:
        score = 7
    elif int(rem) > 1000 and int(rem) < 10000:
        score = 6
    elif int(rem) > 10000 and int(rem) < 100000:
        score = 5
    elif int(rem) > 100000 and int(rem) < 1000000:
        score = 4
    elif int(rem) > 1000000 and int(rem) < 10000000:
        score = 3
    elif int(rem) > 10000000 and int(rem) < 100000000:
        score = 2
    else:
        score = 1
    return score

class FooEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    ...
  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human'):
    ...
  def close(self):
    ...
def possible_choices(bd, d1, d2):
    choices = []

    if (d1 in bd and d2 in bd) and (d1 != d2):
        choices.append(d1)
        choices.append(d2)

    combined = d1 + d2

    if combined in bd:
        choices.append(combined)

    return choices


def play_game(n):
    df_idx = 0
    num_of_successes = 0

    for i in range(n): 
        steps = 0
        board = [1,2,3,4,5,6,7,8,9,10,11,12]
        decision_tree = []
        num_of_choices_made = 0
        
        while board:
            steps = steps + 1
            dice_1 = random.randint(1,6)
            dice_2 = random.randint(1,6)
            options = possible_choices(board, dice_1, dice_2)

            if not options:
                remaining = ''.join(map(str, board))
                final_score = compute_score(remaining)
                #print("game number: ", i)
                #print("finished number: ", remaining, "in", steps, "steps, score: ", final_score)
                
                df.at[df_idx, 'Remainder'] = str(remaining)
                df.at[df_idx, 'Steps'] = steps
                df.at[df_idx, 'Score'] = final_score
                df.at[df_idx, 'Decision_Tree'] = decision_tree
                df.at[df_idx, 'Num_Of_Choices_Made'] = num_of_choices_made 
                break

            else:
                option_str = ','.join(map(str, options))
                str_to_append = ("Step" + str(steps) + ": (" + option_str + ")")
 
                if len(options) == 1:
                    board.remove(options[0])
                    str_to_append = str_to_append + str(options[0])
                elif len(options) == 2:
                    board.remove(options[1])
                    board.remove(options[0])
                    str_to_append = str_to_append + str(options[0]) + "," + str(options[1]) 
                elif len(options) == 3:
                    option_to_pick = random.randint(1,2)
                    num_of_choices_made = num_of_choices_made + 1
                    if option_to_pick == 1:
                        board.remove(options[2])
                        str_to_append = str_to_append + str(options[2])
                    else:
                        board.remove(options[1])
                        board.remove(options[0])
                        str_to_append = str_to_append + str(options[0]) + "," + str(options[1])
                decision_tree.append(str_to_append)

        #print("Decision tree: ", decision_tree)

        if not board:
            final_score = 10
            num_of_successes = num_of_successes + 1
            df.at[df_idx, 'Remainder'] = 'None'
            df.at[df_idx, 'Steps'] = steps
            df.at[df_idx, 'Score'] = final_score
            df.at[df_idx, 'Decision_Tree'] = decision_tree
            df.at[df_idx, 'Num_Of_Choices_Made'] = num_of_choices_made 
            print("SUCCESS IN ", steps, "steps")
            
        df_idx = df_idx + 1

    if num_of_successes > 0:
        success_rate = (num_of_successes / n) * 100
        print("success rate of: ", success_rate, "%")
    else:
        print("no successes")


df = pd.DataFrame(columns=['Remainder', 'Steps', 'Decision_Tree', 'Score', 'Num_Of_Choices_Made'])
play_game(75000)
df.to_csv('data75k.csv', index=False)
print("finished in ", time.time()-start, "seconds")
