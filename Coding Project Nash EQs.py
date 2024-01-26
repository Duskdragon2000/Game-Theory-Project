import random

#=============================================================================
# Project: Given user input or random numbers, generate normal form games and get their nash eqs, payoffs, ect.
#=============================================================================


#Ask user to enter the mode of payoffs entries and then rows/columns and wait for a valid response
def get_user_input():
    mode = input("Enter (R)andom or (M)anual payoffs enteries: ")
    while mode not in ["R", "M"]:
        print("Invalid mode. Please enter either '(R)andom' or '(M)anual'.")
        mode = input("Enter (R)andom or (M)anual payoffs enteries: ")

    rows = int(input("Enter the number of rows: "))
    while not (1 <= rows <= 9):
        print("Invalid number of rows. Please enter a number between 1 and 9.")
        rows = int(input("Enter the number of rows: "))

    columns = int(input("Enter the number of columns: "))
    while not (1 <= columns <= 9):
        print("Invalid number of columns. Please enter a number between 1 and 9.")
        columns = int(input("Enter the number of columns: "))

    return mode, rows, columns

#Random mode payoff generation
def generate_random_payoffs(rows, columns):
    payoffs_p1 = [[random.randint(-99, 99) for _ in range(columns)] for _ in range(rows)]
    payoffs_p2 = [[random.randint(-99, 99) for _ in range(columns)] for _ in range(rows)]

    return payoffs_p1, payoffs_p2

#Manual mode payoff generation. Ask 
def generate_manual_payoffs(rows, columns):
    payoffs_p1 = []
    payoffs_p2 = []
    print("Manual Entries")
    for i in range(rows):
        p1_row = []
        p2_row = []
        for j in range(columns):
            p1_payoff, p2_payoff = input(f"Enter payoff for ( A{i+1}, B{j+1} ) for Player 1 and Player 2: ").split(",")
            p1_row.append(int(p1_payoff))
            p2_row.append(int(p2_payoff))
        payoffs_p1.append(p1_row)
        payoffs_p2.append(p2_row)
    return payoffs_p1, payoffs_p2

#Displays normal form by combining both payoff sets and formats it as well.
def display_normal_form(rows, columns, payoffs_p1, payoffs_p2):

    print("=" * 40)
    print("Display Normal Form")
    print("=" * 40)
    print(" " * 9 + " ".join(f"B{j+1:<10}" for j in range(columns)))
    print(" " * 3 + "-" * (columns * 12 + 1))
    for i in range(rows):
        print(f"A{i+1} ", end="")
        for j in range(columns):
            print(f"| ({payoffs_p1[i][j]:>3},{payoffs_p2[i][j]:>3}) ", end="")
        print("|")
        print(" " * 3 + "-" * (columns * 12 + 1))


#Calculate the nash eq by comparing best responses
def calculate_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2):
    best_responses_p1 = [max(column) for column in zip(*payoffs_p1)]
    best_responses_p2 = [max(row) for row in payoffs_p2]

    nash_equilibria = []
    for i in range(rows):
        for j in range(columns):
            if payoffs_p1[i][j] == best_responses_p1[j] and payoffs_p2[i][j] == best_responses_p2[i]:
                nash_equilibria.append((i, j))

    return nash_equilibria

#Displays nash eq like normal from but replaces it with H,H
def display_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2, nash_equilibria):
    player1_strategies = [f"A{i+1}" for i in range(rows)]
    player2_strategies = [f"B{j+1}" for j in range(columns)]

    if nash_equilibria:
        print("=" * 40)
        print("Nash Pure Equilibrium Locations")
        print("=" * 40)
        print(" " * 9 + " ".join(f"B{j+1:<11}" for j in range(columns)))
        print(" " * 3 + "-" * (columns * 12 + 1))


        for i in range(rows):
            row = [player1_strategies[i]]
            for j in range(columns):
                if (i, j) in nash_equilibria:
                    row.append("| ( H , H ) ")
                else:
                    row.append(f"| ({payoffs_p1[i][j]:>3},{payoffs_p2[i][j]:>3}) ")
                    
            print(" ".join(row) + "|")
            print(" " * 3 + "-" * (columns * 12 + 1))

        print("Nash Pure Equilibrium(s):", end=" ")
        for i, j in nash_equilibria:
            print(f"({player1_strategies[i]}, {player2_strategies[j]})", end=" ")
        print()

    else:
        display_normal_form_with_best_responses(rows, columns, payoffs_p1, payoffs_p2)
        
#Called when there are no pure nash eqs and continues to replace best response with H
def display_normal_form_with_best_responses(rows, columns, payoffs_p1, payoffs_p2):
    player1_strategies = [f"A{i+1}" for i in range(rows)]
    player2_strategies = [f"B{j+1}" for j in range(columns)]

    best_responses_p1 = [max(column) for column in zip(*payoffs_p1)]
    best_responses_p2 = [max(row) for row in payoffs_p2]

    print("="*40)
    print("Nash Pure Equilibrium Locations")
    print("=" * 40)
    print(" " * 9 + " ".join(f"B{j+1:<10}" for j in range(columns)))
    print(" " * 3 + "-" * (columns * 12 + 1))
    for i in range(rows):
        row = [f"{player1_strategies[i]} |"]
        for j in range(columns):
            if payoffs_p1[i][j] == best_responses_p1[j] and payoffs_p2[i][j] == best_responses_p2[i]:
                row.append(" ( H , H ) |")
            elif payoffs_p1[i][j] == best_responses_p1[j]:
                row.append(f" ( H ,{payoffs_p2[i][j]:>3}) |")
            elif payoffs_p2[i][j] == best_responses_p2[i]:
                row.append(f" ({payoffs_p1[i][j]:>3}, H ) |")
            else:
                row.append(f" ({payoffs_p1[i][j]:>3},{payoffs_p2[i][j]:>3}) |")
        print("".join(row))
        print(" " * 3 + "-" * (columns * 12 + 1))

    nash_equilibria = []
    for i in range(rows):
        for j in range(columns):
            if payoffs_p1[i][j] == best_responses_p1[j] and payoffs_p2[i][j] == best_responses_p2[i]:
                nash_equilibria.append((player1_strategies[i], player2_strategies[j]))
    if len(nash_equilibria) > 0:
        print("Nash Pure Equilibrium(s):", " ".join([f"({ne[0]}, {ne[1]})" for ne in nash_equilibria]))
    else:
        print("Nash Pure Equilibrium(s): None")

#Creates random beliefs 
def create_random_beliefs(rows, columns):
    belief_p1 = [random.random() for _ in range(columns)]
    belief_p1 = [p / sum(belief_p1) for p in belief_p1]

    belief_p2 = [random.random() for _ in range(rows)]
    belief_p2 = [p / sum(belief_p2) for p in belief_p2]

    return belief_p1, belief_p2

#Explected payofs given beliefs and payoffs
def calculate_expected_payoffs(rows, columns, payoffs_p1, payoffs_p2, belief_p1, belief_p2):
    expected_payoffs_p1 = [sum(payoffs_p1[i][j] * belief_p1[j] for j in range(columns)) for i in range(rows)]
    expected_payoffs_p2 = [sum(payoffs_p2[i][j] * belief_p2[i] for i in range(rows)) for j in range(columns)]

    return expected_payoffs_p1, expected_payoffs_p2

#Find best response
def find_best_responses(expected_payoffs_p1, expected_payoffs_p2):
    best_response_p1 = max(expected_payoffs_p1)
    best_response_indices_p1 = [i for i, payoff in enumerate(expected_payoffs_p1) if payoff == best_response_p1]

    best_response_p2 = max(expected_payoffs_p2)
    best_response_indices_p2 = [j for j, payoff in enumerate(expected_payoffs_p2) if payoff == best_response_p2]

    return best_response_indices_p1, best_response_indices_p2

#Get indifference probibility
def calculate_indifference_probabilities(payoffs_p1, payoffs_p2):
    
    # Calculate player 1's indifference probability
    p1_prob = (payoffs_p2[1][0] - payoffs_p2[1][1]) / ((payoffs_p2[0][1] - payoffs_p2[1][1]) - (payoffs_p2[0][0] - payoffs_p2[1][0]))
    
    # Calculate player 2's indifference probability
    p2_prob = (payoffs_p1[0][1] - payoffs_p1[1][1]) / ((payoffs_p2[0][0] - payoffs_p2[1][0]) - (payoffs_p2[0][1] - payoffs_p2[1][1]))
    
    # Format and display 
    print("-" * 40)
    print("Player 1 & 2 Indifferent Mix Probabilities")
    print("-" * 40)
    print(f"Player 1 probability of strategies (A1) = {p1_prob:.2f}")
    print(f"Player 1 probability of strategies (A2) = {1-p1_prob:.2f}")
    print(f"Player 2 probability of strategies (B1) = {p2_prob:.2f}")
    print(f"Player 2 probability of strategies (B2) = {1-p2_prob:.2f}")

# Calculate expected payoffs for both players mixing by the random beliefs 
def calculate_expected_payoffs_both_players_mix(num_strategies_p1, num_strategies_p2, payoffs_p1, payoffs_p2, belief_p1, belief_p2):
    
    # Calculate expected payoffs for both players
    expected_payoffs_p1 = sum(belief_p2[j] * sum(payoffs_p1[i][j] * belief_p1[i] for i in range(num_strategies_p1)) for j in range(num_strategies_p2))
    
    expected_payoffs_p2 = sum(belief_p1[i] * sum(payoffs_p2[i][j] * belief_p2[j] for j in range(num_strategies_p2)) for i in range(num_strategies_p1))
    
    # Format and display the results
    print("-" * 40)
    print("Player 1 & 2 Expected Payoffs with both Players Mixing")
    print("-" * 40)
    print(f"Player 1 -> U({', '.join([f'{bel:.2f}' for bel in belief_p1])}), ({', '.join([f'{bel:.2f}' for bel in belief_p2])}) = {expected_payoffs_p1:.2f}")
    print(f"Player 2 -> U({', '.join([f'{bel:.2f}' for bel in belief_p1])}), ({', '.join([f'{bel:.2f}' for bel in belief_p2])}) = {expected_payoffs_p2:.2f}")


#Expected payoffs mixing with eachother and formated
def print_expected_payoffs_p1p2(rows, columns, player1_strategies, belief_p1, expected_payoffs_p1, player2_strategies, belief_p2, expected_payoffs_p2):

    print("-" * 40)
    print("Player 1 Expected Payoffs with Player 2 Mixing")
    print("-" * 40)
    for i in range(rows):
        print(f"U({player1_strategies[i]},({','.join(f'{p:.2f}' for p in belief_p1)})) = {expected_payoffs_p1[i]:.2f}")
    print()

    print("-" * 40)
    print("Player 1 Best Response with Player 2 Mixing")
    print("-" * 40)
    print(f"BR({','.join(f'{p:.2f}' for p in belief_p1)}) = {{{','.join(player1_strategies[i] for i in best_response_indices_p1)}}}")
    print()

    print("-" * 40)
    print("Player 2 Expected Payoffs with Player 1 Mixing")
    print("-" * 40)
    for j in range(columns):
        print(f"U(({','.join(f'{p:.2f}' for p in belief_p2)}),{player2_strategies[j]}) = {expected_payoffs_p2[j]:.2f}")
    print()

    print("-" * 40)
    print("Player 2 Best Response with Player 1 Mixing")
    print("-" * 40)
    print(f"BR({','.join(f'{p:.2f}' for p in belief_p2)}) = {{{','.join(player2_strategies[j] for j in best_response_indices_p2)}}}")
    print()

#Display payoffs
def display_payoffs(rows, columns, payoffs_p1, payoffs_p2 ):

    # Display strategy spaces and payoffs
    p1_strategies = ["A" + str(i+1) for i in range(rows)]
    p2_strategies = ["B" + str(j+1) for j in range(columns)]

    print("--------------------------------------")
    print("Player: Player1's strategies")
    print("--------------------------------------")
    print("{", end="")
    for i in range(rows):
        print(p1_strategies[i], end="")
        if i != rows-1:
            print(",", end=" ")
    print("}")
    print()

    print("--------------------------------------")
    print("Player: Player1's payoffs")
    print("--------------------------------------")
    for i in range(rows):
        for j in range(columns):
            print("{: >6}".format(str(payoffs_p1[i][j])), end="")
        print()
    print()

    print("--------------------------------------")
    print("Player: Player2's strategies")
    print("--------------------------------------")
    print("{", end="")
    for j in range(columns):
        print(p2_strategies[j], end="")
        if j != columns-1:
            print(",", end=" ")
    print("}")
    print()

    print("--------------------------------------")
    print("Player: Player2's payoffs")
    print("--------------------------------------")
    for i in range(rows):
        for j in range(columns):
            print("{: >6}".format(str(payoffs_p2[i][j])), end="")
        print()
    print()


#Where main starts, but this is python so theres no main :(

mode, rows, columns = get_user_input()

#random mode
if mode == "R":


    payoffs_p1, payoffs_p2 = generate_random_payoffs(rows, columns) # enerate random payoffs for player 1 and player 2

    display_payoffs(rows, columns, payoffs_p1, payoffs_p2 ) #Display the payoffs

    display_normal_form(rows, columns, payoffs_p1, payoffs_p2) #Display normal form 
    print()

    nash_equilibria = calculate_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2) #Calculate the Nash eq 

    display_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2, nash_equilibria) #Display the Nash eq of the game
    print() 
    
    belief_p1, belief_p2 = create_random_beliefs(rows, columns) #Generate random beliefs 

    expected_payoffs_p1, expected_payoffs_p2 = calculate_expected_payoffs(rows, columns, payoffs_p1, payoffs_p2, belief_p1, belief_p2)  #Expected payoffs based on those beliefs
    
    best_response_indices_p1, best_response_indices_p2 = find_best_responses(expected_payoffs_p1, expected_payoffs_p2) #Find best responses based on their expected payoffs 

    player1_strategies = [f"A{i+1}" for i in range(rows)]      # Create a list of strategies 
    player2_strategies = [f"B{j+1}" for j in range(columns)]

    print_expected_payoffs_p1p2(rows, columns, player1_strategies, belief_p1, expected_payoffs_p1, player2_strategies, belief_p2, expected_payoffs_p2) # Print the expected payoffs based on their beliefs

    num_strategies_p1 = len(payoffs_p1)
    num_strategies_p2 = len(payoffs_p2)
    calculate_expected_payoffs_both_players_mix(num_strategies_p1, num_strategies_p2, payoffs_p1, payoffs_p2, belief_p1, belief_p2)  #Expected payoffs for both players when both players play mixed strategies
    print()
    

    #For random mode 2x2 game
    if rows == 2 and columns == 2: 

        # Check if there is a Pure Nash Equilibrium
        nash_equilibria = calculate_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2)
        if not nash_equilibria:
            # Calculate the indifference probabilities
            calculate_indifference_probabilities(payoffs_p1, payoffs_p2)
        else:
            print("-" * 40)
            print("Player 1 & 2 Indifferent Mix Probabilities")
            print("-" * 40)
            print("Normal Form has Pure Strategy Equilibrium ")
            print()

#manual mode
else:

    payoffs_p1, payoffs_p2 = generate_manual_payoffs(rows, columns) #get the manual payoffs 

    display_normal_form(rows, columns, payoffs_p1, payoffs_p2) #display normal form 
    print()

    nash_equilibria = calculate_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2) #get nash eq

    display_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2, nash_equilibria) #display nash eq
    print()

    #for Manual mode 2x2 game
    if rows == 2 and columns == 2: 

        # Check if there is a Pure Nash Equilibrium
        nash_equilibria = calculate_nash_equilibria(rows, columns, payoffs_p1, payoffs_p2)
        if not nash_equilibria:
            # Calculate the indifference probabilities
            calculate_indifference_probabilities(payoffs_p1, payoffs_p2)
        else:
            print("-" * 40)
            print("Player 1 & 2 Indifferent Mix Probabilities")
            print("-" * 40)
            print("Normal Form has Pure Strategy Equilibrium ")
            print()


