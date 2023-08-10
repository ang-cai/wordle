'''
[CS1] Wordle- Guess a five-letter secret word in at most six attempts.
'''
import random
# To install colorama, run the following command in your VS Code terminal:
# py -m pip install colorama
from colorama import Fore, Back, Style, init
init(autoreset=True) #Ends color formatting after each print statement
from wordle_wordlist import get_word_list


def pick_secret_word(word_list: list[str]) -> str:
    '''Picks a secret word from the list of allowable words

        Returns:
            str: a single word from the list of allowable words
    '''
    return random.choice(word_list)
    # return "GAUDY"  # Sample word for testing.

def get_player_guess(word_list: list[str]) -> str:
    '''Prompts for and returns a player guess until the player enters a guess that:
        - is exactly five letters
        - exists in the list of Wordle words
        Args:
            word_list (list): A list of allowable words
        Returns:
            str: a string guess that is exactly 5 uppercase letters.
    '''
    guess = input("Enter guess: ")
    while len(guess) != 5 or guess.upper() not in word_list:
        guess = input("Enter a valid guess: ")

    return guess.upper()

def get_AI_guess(word_list: list[str], guesses: list[str], feedback: list[str]) -> str:
    '''Analyzes feedback from previous guesses (if any) to make a new guess
        Args:
            word_list (list): A list of potential Wordle words
            guesses (list): A list of string guesses, could be empty
            feedback (list): A list of feedback strings, could be empty
        Returns:
         str: a valid guess that is exactly 5 uppercase letters
    '''
    correct_letters = []
    incorrect_letters = []
    correct_place = {}
    incorrect_place = {}


    if guesses == []:
        return "CRATE"
    
    for i in range(len(feedback)):
        word = feedback[i]
        cor_word = guesses[i]
        for j in range(len(word)):
            if word[j] != "-" and word[j].upper() not in correct_letters:
                correct_letters += [word[j].upper()]
                if word[j].upper() in incorrect_letters:
                    incorrect_letters.remove(cor_word[j])
            if word[j] == "-":
                if cor_word[j].upper() not in correct_letters and cor_word[j].upper() not in incorrect_letters:
                    incorrect_letters += cor_word[j]

            if word[j].isupper() and word[j] in correct_place:
                correct_place[word[j]] += [j]
            if word[j].isupper() and word[j] not in correct_place:
                correct_place[word[j]] = [j]
            if word[j].islower() and cor_word[j] in incorrect_place:
                incorrect_place[cor_word[j]] += [j]
            if word[j].islower() and cor_word[j] not in incorrect_place:
                incorrect_place[cor_word[j]] = [j]

    for word in word_list:
        if all(letter in word for letter in correct_letters) and all(letter not in word for letter in incorrect_letters) and word not in guesses:
            correct_green = True
            different_yellow = True
            for item in correct_place:
                for number in correct_place[item]:
                    if word[number] != item:
                        correct_green = False
            
            for item in incorrect_place:
                for number in incorrect_place[item]:
                    if word[number] == item:
                        different_yellow = False

            if correct_green and different_yellow:
                return word
 

def get_feedback(guess: str, secret_word: str) -> str:
    '''Generates a feedback string based on comparing a 5-letter guess with the secret word. 
       The feedback string uses the following schema: 
        - Correct letter, correct spot: uppercase letter ('A'-'Z')
        - Correct letter, wrong spot: lowercase letter ('a'-'z')
        - Letter not in the word: '-'

       For example:
        - get_feedback("lever", "EATEN") --> "-e-E-"
        - get_feedback("LEVER", "LOWER") --> "L--ER"
        - get_feedback("MOMMY", "MADAM") --> "M-m--"
        - get_feedback("ARGUE", "MOTTO") --> "-----"

        Args:
            guess (str): The guessed word
            secret_word (str): The secret word
        Returns:
            str: Feedback string, based on comparing guess with the secret word
    '''
    feedback = ""
    guess = str(guess).upper()
    secret_word = secret_word.upper()

    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback += f"{guess[i]}"
        elif guess[i] in secret_word:
            if guess.count(guess[i], 0, i+1) <= secret_word.count(guess[i]):
                feedback += f"{guess[i].lower()}"
            else:
                feedback += "-"
        else:
            feedback += "-"

    for i in range(len(feedback)):
        if (feedback.count(feedback[i]) + feedback.count(feedback[i].upper())) > secret_word.count(feedback[i].upper()) and feedback[i] != secret_word[i]:
            feedback = feedback.replace(f"{feedback[i]}", "-", 1)
    return feedback

def print_feedback(guesses: list[str], feedback: list[str]):
    '''Uses the colorama library to display the history of guesses and their corresponding feedback.
        - Green/White: Correct letter in the correct spot
        - Yellow/White: Correct letter in the incorrect spot
        - Black/White: Guessed letters not in the word

        For example, if you guess "LEVER" when the secret word is "EATEN":
         - The first E turns Yellow because it is in the secret word but in the wrong spot.
         - The second E turns Green because it is in the secret word, and in the correct spot.
         - The other letters (L, V, R) will turn Black because they are not in the secret word.

        If you guess two of the same letter in a word, and only one of the letters turn Yellow
        or Green, then there is only one copy of that letter in the secret word.

        Args:
            guesses (list): A list of guessed words
            feedback (list): A list of feedback strings
    '''
    print(Back.WHITE + Fore.WHITE + "       ")
    for i in range(len(guesses)):
        color_string = Back.WHITE + Fore.WHITE + " "
        for j in range(5):
            if feedback[i][j] == "-":
                color_string += Back.BLACK+Fore.WHITE + guesses[i][j]
            elif ord(feedback[i][j]) < 97:  # Checks if this character is an UPPERCASE letter.
                color_string += Back.GREEN+Fore.WHITE + feedback[i][j]
            else:
                color_string += Back.YELLOW+Fore.WHITE + feedback[i][j].upper()
        color_string += Back.WHITE+Fore.WHITE + " "
        print(color_string)
    print(Back.WHITE + Fore.WHITE + "       ")

def play_wordle(secret_word: str, word_list: list[str], mode="HUMAN") -> list[str]:
    '''Plays a complete game of Wordle. The game ends when:
        - a player has guessed the secret word
        - a player has not guessed the secret word in six guesses

        if mode == "AI", the AI should make guesses.
        if mode == "HUMAN", a human should make guesses.

        Args:
            secret_word (str): The secret word
            word_list (list): A list of allowable words
            mode (str): The mode (HUMAN or AI) of play
        Returns:
         list: a list of all valid player guesses
    '''
    guesses = []
    feedback = []
    
    if mode == "HUMAN":
        for i in range(6):
            guess = get_player_guess(word_list)
            formatted = get_feedback(guess, secret_word)
            guesses += [guess]
            feedback += [formatted]
            print_feedback(guesses, feedback) 
            while guess == secret_word:
                return guesses
        return guesses
    
    if mode == "AI":
        for i in range(6):
            guess = get_AI_guess(word_list, guesses, feedback)
            formatted = get_feedback(guess, secret_word)
            guesses += [guess]
            feedback += [formatted]
            print_feedback(guesses, feedback) 
            while guess == secret_word:
                return guesses
        return guesses 

if __name__ == "__main__":
    secret_word = pick_secret_word(get_word_list()) # Sometimes secret_word will be easy, sometimes will be hard
    play_wordle(secret_word, get_word_list(), "AI")
        
    guesses = play_wordle(secret_word, get_word_list(), "AI")

    # TODO (Exercise 2b): Write code below to determine whether the player won or lost.
    if secret_word in guesses:
        print("You win!")
    else:
        print(f"The word was {secret_word}.")

    