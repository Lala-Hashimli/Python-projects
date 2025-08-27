# def functions
def default_game(attemps, underscores, alphabet, user_choice, stages):
    if attemps == 7:
        print(stages[0])
        print(f"""
----------------------------------------
    About: {user_choice}\n
    {underscores}\n
    {alphabet}
        """)


# correct guess

def correct_guess(random_word, stages, wrong_guesses, len_word, user_letter, underscores):
    print(stages[wrong_guesses])
    underscores = list(underscores)

    for index in range(len_word):
        is_letter_match = random_word[index] == user_letter

        if is_letter_match: 
            underscores[index] = user_letter if is_letter_match else underscores[index]

    return "".join(underscores) 


# wrong guess

def failed_attempts(attemps, wrong_guesses, stages):
    attemps -= 1
    wrong_guesses += 1
    print(stages[wrong_guesses])
    return attemps, wrong_guesses

# used letter
def remove_used_letter(alphabet, user_letter):
    alphabet_list = list(alphabet)
    alphabet_list.remove(user_letter)
    return "".join(alphabet_list)

# VICTORYYYYYY
def show_victory(stages, user_choice, underscores,chance, streak):
    streak += 1
    print(f"""
    {stages[-1]}
---------------------------------------------------
    Streak: {streak}
    Chance: {chance}\n
        About: {user_choice}\n
        {underscores}
    """)
    return streak
# game over :(((

def show_game_over(stages, user_choice, random_word, chance, streak):
    chance-=1
    print(f"""
    {stages[7]}
    UNFORTUNATELY, HANGMAN DIED :(
---------------------------------------------------    
    Chance: {chance}\n
    Streak: {streak}\n
        About: {user_choice}\n
        {random_word}
    """)
    return chance

