from os import system
from string import ascii_uppercase
from random import choice
from hangman_data import *

attemps = 7
wrong_guesses = 0 
alphabet = ascii_uppercase
user_choice = input(f"""
Choose a category
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

# default 
if attemps == 7:
    print(stages[0])
    print(f"""
    ------------------------------
        About: {user_choice}\n
        {underscores}\n
        {alphabet}
""")


while attemps > 0:
    user_letter = input("Please, enter letter: \n>>").upper()

    # eger reqem ve ya 2 dene herf daxil edilibse
    if not user_letter.isalpha() or len(user_letter) != 1:
        print("Whoa! That’s too much, try one letter only, please")
        continue

    if user_letter not in alphabet:
        print("Hey! That letter’s been guessed. Pick another.")
        continue

    # istifadecinin daxil elediyi herf random sozde varsa
    if user_letter in random_word:
        system("clear")
        print(stages[wrong_guesses])
        underscores = list(underscores)

        for index in range(len_word):
            is_letter_match = random_word[index] == user_letter

            if is_letter_match: 
                underscores[index] = user_letter if is_letter_match else underscores[index]

        underscores = "".join(underscores)   

    else:
        system("clear")
        attemps -= 1
        wrong_guesses += 1
        print(stages[wrong_guesses])
    
   
    

    alphabet = list(alphabet)
    alphabet.remove(user_letter)
    new_alphabet = "".join(alphabet)
    
    print(f"""
    ------------------------------
        
        About: {user_choice}\n
        {underscores}\n
        {new_alphabet}
    """)

    # qalib gelnde
    if underscores == random_word:
        system("clear")
        print(f"""
        {stages[-1]}
---------------------------------------------------
        About: {user_choice}\n
        {underscores}
        """)
        exit()

else:
    # uduzunda
    system("clear")
    print(f"""
        {stages[7]}
    UNFORTUNATELY, HANGMAN DIED :(
---------------------------------------------------    
        About: {user_choice}\n
        {random_word}
    """)

    