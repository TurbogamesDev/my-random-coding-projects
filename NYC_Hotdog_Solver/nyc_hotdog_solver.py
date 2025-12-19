import random

all_combinations = []
combination = [None, None, None, None, None, None, None, None]
combination_matches = {}
combination_to_do = "XXXX____"

remaining_combinations = {}
remaining_combinations_matches = {}

a = 0
b = 1
c = 2
d = 3

def get_combination(p, q, r, s):
    new_combination = [None, None, None, None, None, None, None, None]
    new_combination[p] = True
    new_combination[q] = True
    new_combination[r] = True
    new_combination[s] = True
    
    return new_combination

def combination_to_string(com):
    return_var = ""

    for val in com:
        if val:
            return_var += "X"
        else:
            return_var += "_"
    
    return return_var

def string_to_combination(str):
    return_var = []

    for letter in str:
        if letter == "X":
            return_var.append(True)
        elif letter == "_":
            return_var.append(False)
    
    return return_var

while a < 5:
    while b < 6:
        while c < 7:
            while d < 8:
                all_combinations.append(get_combination(a, b, c, d))
                d += 1
            c += 1
            d = c + 1
        b += 1
        c = b
    a += 1
    b = a

remaining_combinations = all_combinations

for com in all_combinations:
    output = ""
    for val in com:
        if val:
            output += "X"
        else:
            output += "_"
    print(output)

for p in all_combinations:
    combination_matches.update({combination_to_string(p): {"0": [], "1": [], "2": [], "3": [], "4": []}})

    for q in all_combinations:
        correct_choices = 0

        for num in range(8):
            if p[num] and q[num]:
                correct_choices += 1

        combination_matches[combination_to_string(p)][str(correct_choices)].append(combination_to_string(q))

remaining_combinations_matches = combination_matches
        
while True:
    print("Do this combination:")
    print(combination_to_do[:4])
    print(combination_to_do[4:])
    user_input = input("How many were correct?: ")

    if user_input == "4":
        exit()

    remaining_combinations = remaining_combinations_matches[combination_to_do][user_input]

    temp = {}

    for p_com in remaining_combinations:
        p = string_to_combination(p_com)
        temp.update({combination_to_string(p): {"0": [], "1": [], "2": [], "3": [], "4": []}})

        for q_com in remaining_combinations:
            q = string_to_combination(q_com)
            correct_choices = 0

            for num in range(8):
                if p[num] and q[num]:
                    correct_choices += 1

            temp[combination_to_string(p)][str(correct_choices)].append(combination_to_string(q))
    
    remaining_combinations_matches = temp

    best_suited_combination_guess = ""
    best_suited_combination_guess_length = 71

    for com in remaining_combinations:
        if len(remaining_combinations_matches[com]["2"]) < best_suited_combination_guess_length:
            best_suited_combination_guess_length = len(remaining_combinations_matches[com]["2"])
            best_suited_combination_guess = com
    
    combination_to_do = best_suited_combination_guess




        



# selected_combination = random.choice(all_combinations)



# while True:
#     user_input = input("enter a guess")
#     user_input_parsed = []

#     for i in user_input:
#         if i == "X":
#             user_input_parsed.append(True)
#         elif i == "_":
#             user_input_parsed.append(False)
    
#     print(user_input_parsed)

#     correct_choices = 0

#     for num in range(len(selected_combination)):
#         if selected_combination[num] == user_input_parsed[num]:
#             correct_choices += 1

#     print(f"({correct_choices}/4)")
