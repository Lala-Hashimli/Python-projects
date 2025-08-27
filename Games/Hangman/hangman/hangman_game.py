from os import system
from string import ascii_uppercase
from random import choice
from time import sleep
from hangman_data import *
from hangman_def import *



chance = 5
streak = 0
def play_game(chance, streak):
    attemps = 7
    wrong_guesses = 0 
    alphabet = ascii_uppercase

    system("clear")
    user_choice = input(f"""
Choose a category:
(musics, movies, video games, colors, countries, technologies, random):\n>> """)


    if user_choice in categories:
        random_word = choice(categories[user_choice])
    elif user_choice == "random":
        random_catagory = choice(list(categories.keys()))
        random_word = choice(categories[random_catagory])
    else:
        print("Oops! That's not a valid category. Try again")
        

    len_word = len(random_word)
    underscores = "_" * len_word

    default_game(attemps, underscores, alphabet, user_choice, stages)

    while attemps > 0:
        user_letter = input("Please, enter letter: \n>>").upper()
        

        # eger reqem ve ya 2 dene herf daxil edilibse
        if not user_letter.isalpha() or len(user_letter) != 1:
            print("Whoa! That’s too much, try one letter only, please")
            continue
        
        # tekrar herf daxil etme xetasının qarşisini  aliriq
        if user_letter not in alphabet:
            print("Hey! That letter’s been guessed. Pick another.")
            continue

        # istifadecinin daxil elediyi herf random sozde varsa
        if user_letter in random_word:
            system("clear")
            underscores = correct_guess(random_word, stages, wrong_guesses, len_word, user_letter, underscores)
        else:
            system("clear")
            attemps, wrong_guesses = failed_attempts(attemps, wrong_guesses, stages)

        
        alphabet = remove_used_letter(alphabet, user_letter)

        print(f"""
    ------------------------------
        
    About: {user_choice}\n
    {underscores}\n
    {alphabet}
        """)

        # victorryy
        game_won = (underscores == random_word)
        if game_won:
            system("clear")
            streak = show_victory(stages, user_choice, underscores, chance, streak)
            break 

    else:
        # game over
        system("clear")
        chance = show_game_over(stages, user_choice, random_word, chance, streak)
    return streak, chance

while chance > 0:
    streak, chance = play_game(chance, streak)
    user_answer = input("Do you want to play again?(yes/no) \n>> ")
    if user_answer == "yes":
        system("clear")
        for time in range(1, 4):
            print(f"Game will start after {time} seconds..")
            sleep(1)
    else:
        system("clear")
        print("BYEEE, SEE YOU LATTERRR")
        print(f"""
        Streak: {streak}
        Chance: {chance}
    """)
        exit()
else:
    print("You do not enough chance")