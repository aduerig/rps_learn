import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_result(a, b):
    if a == b:
        return 0
    
    if b == 'r' and a == 'p':
        return 1
    if a == 'r' and b == 'p':
        return -1

    if b == 'p' and a == 's':
        return 1
    if a == 'p' and b == 's':
        return -1

    if a == 's' and b == 'r':
        return -1
    if b == 's' and a == 'r':
        return 1
    raise Exception('idk')

result_to_string = {
    -1: 'You won',
    0: 'We tied',
    1: 'You lost',
}

all_human_guesses = {}
human_wins = {}

opposite_winning = {
    'r': 'p',
    'p': 's',
    's': 'r',
}

def get_guess_from_history(player_name):
    depth = 7

    if player_name not in all_human_guesses:
        return random.choice(['r', 'p', 's'])
    current_player_guesses = all_human_guesses[player_name]

    final_chances = {'r': 0, 's': 0, 'p': 0}
    base_counts = {'r': 0, 's': 0, 'p': 0}
    for guess in base_counts.keys():
        base_counts[guess] = current_player_guesses.count(guess) + 1
    all_possible = sum(base_counts.values())
    for guess in base_counts.keys():
        final_chances[guess] = base_counts[guess] / all_possible
    print(final_chances)

    n_grams = {}
    for length in range(1, depth):
        if length not in n_grams:
            n_grams[length] = {}
        curr_gram = n_grams[length]
        for i in range(len(current_player_guesses) - length):
            seq = ''.join(current_player_guesses[i:i+length])
            answer = current_player_guesses[i+length]
            if seq not in curr_gram:
                curr_gram[seq] = {'r': 1, 's': 1, 'p': 1}
            curr_gram[seq][answer] += 1

    print(current_player_guesses)
    for guess in ['r', 'p', 's']:
        for length in range(1, min(depth, len(current_player_guesses) + 1)):
            curr_gram = n_grams[length]
            seq = ''.join(current_player_guesses[-length:])
            if seq not in curr_gram:
                continue
            all_times = sum(curr_gram[seq].values())
            print(seq, curr_gram[seq])
            final_chances[guess] *= curr_gram[seq][guess] / all_times
            # all_at_depth = sum(map(lambda x: sum(x.values()), curr_gram.values()))

    print(final_chances)
    best_opponant_guess = random.choices(['r', 'p', 's'], k=1, weights=[final_chances['r'], final_chances['p'], final_chances['s']])[0]
    return opposite_winning[best_opponant_guess]


def update_history(player_name, guess):
    if player_name not in all_human_guesses:
        all_human_guesses[player_name] = []
    
    current_player_guesses = all_human_guesses[player_name]
    current_player_guesses.append(guess)

    if len(current_player_guesses) > 300:
        current_player_guesses = current_player_guesses[150:]

guess_to_str = {
    'r': 'rock',
    's': 'scissors',
    'p': 'paper',
}

def get_response_string_from_guess(player_name, human_guess):
    if human_guess not in ['r', 'p', 's']:
        return ''
    
    computer_guess = get_guess_from_history(player_name)
    result = get_result(computer_guess, human_guess)
    if player_name not in human_wins:
        human_wins[player_name] = 0    
    human_wins[player_name] += ((-result) + 1) / 2
    update_history(player_name, human_guess)
    return f'I threw {guess_to_str[computer_guess]}. ' + result_to_string[result] + f', your winrate is {100 * (human_wins[player_name] / len(all_human_guesses[player_name])):,.2f}%'

if __name__ == '__main__':
    result_to_string_colored = {
        -1: f'{bcolors.OKGREEN}You won',
        0: f'{bcolors.OKCYAN}We tied',
        1: f'{bcolors.FAIL}You lost',
    }
 
    while True:
        player_name = 'local'
        human_guess = input('Your guess? Options are r, p, or s\n').lower().strip()

        if human_guess not in ['r', 'p', 's']:
            print('couldnt understant')
            continue
        
        computer_guess = get_guess_from_history(player_name)
        result = get_result(computer_guess, human_guess)
        if player_name not in human_wins:
            human_wins[player_name] = 0    
        human_wins[player_name] += ((-result) + 1) / 2
        update_history(player_name, human_guess)
        print(result_to_string_colored[result] + f'{bcolors.ENDC}, your winrate is {100 * (human_wins[player_name] / len(all_human_guesses[player_name])):,.2f}%')
