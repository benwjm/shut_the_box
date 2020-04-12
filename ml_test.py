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


def check_combination_possibility(bd, combined):
    combination_possibilities = []
    for i in range(len(bd)):
        initial = bd[i]
        for y in range(i, len(bd)):
            combo = bd[i] + bd[y]
            if combo == combined and bd[i] != bd[y]:
                combination_possibilities.append((bd[i],bd[y]))

    return combination_possibilities
    

def possible_choices(bd, d1, d2):
    choices = []

    combined = d1 + d2

    all_combos = check_combination_possibility(bd, combined)
    for i in range(len(all_combos)):
        choices.append(all_combos[i])
    if combined in bd:
        choices.append(combined)

    #print("all choices: ", choices)
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
            #print(dice_1 + dice_2)
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
                str_to_append = ("Step" + str(steps) + ": [" + option_str + "]")
                if len(options) == 1:
                    if type(options[0]) is tuple:
                        board.remove(options[0][1])
                        board.remove(options[0][0])
                    else:
                        board.remove(options[0])
                        str_to_append = str_to_append + " " + str(options[0])
                else:
                    num_of_choices_made = num_of_choices_made + 1
                    selection = options[random.randint(0,len(options)-1)]
                    str_to_append = str_to_append + " " + str(selection)
                    if type(selection) is tuple:
                        board.remove(selection[1])
                        board.remove(selection[0])
                    else:
                        board.remove(selection)
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
play_game(100000)
df.to_csv('data100k.csv', index=False)
print("finished in ", time.time()-start, "seconds")
