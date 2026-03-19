# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for item in secret_word:
      if item not in letters_guessed:
        return False
    return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    ret_str =[]
    for i in range(len(secret_word)):
      ret_str.append('_ ')

    for i in range(len(letters_guessed)):
      if letters_guessed[i] in secret_word :
        search_ch = letters_guessed[i]
        for j in range(len(secret_word)):
          if secret_word[j] ==search_ch:
            ret_str[j] = search_ch

    return ''.join(ret_str)

import string


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    alphabet = string.ascii_lowercase
    ret_str =''
    for item in alphabet :
      if item not in letters_guessed:
        ret_str +=item
    return ret_str

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guess_num =6
    warning_num =3

    letters_guessed =[]

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is',len(secret_word),'letters long.')
      
    while guess_num >0 and not is_word_guessed(secret_word,letters_guessed):
      is_warning = True
      is_wrong = True

      print('You have',guess_num,'guesses left')
      print(get_guessed_word(secret_word,letters_guessed))
      print(get_available_letters(letters_guessed))
      user_input = input('Please guess a letter:')

      if user_input.isalpha():
        if user_input not in letters_guessed:
          is_warning =False
          letters_guessed.append(user_input)
          if user_input in secret_word:
            is_wrong =False
            print('Good Guess')
      if is_warning:
        if user_input.isalpha():
          print('Already guessed that')
        else:
          print('Enter only characters')
        if warning_num:
          warning_num-=1
          print('You have',warning_num,'warnings left')
        else:
          guess_num-=1
        
      elif is_wrong:
        print('Wrong Guess')
        if user_input in 'aeouiy':
          guess_num-=2
        else:
          guess_num-=1

    if is_word_guessed(secret_word,letters_guessed):
    
      print("You won!")
    else:
      print('You lost!!')
      print('Word is:',secret_word)
    unique_str =''
    for item in secret_word:
      if item not in unique_str:
        unique_str+=item 
  
    print('Score:',guess_num*len(unique_str))


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    word =''
    for item in my_word:
      if item != ' ':
        word +=item
    if len(word)==len(other_word):
      for i in range(len(word)):
        if word[i]!='_' and word[i]!=other_word[i]:
          return False
      return True
    
    return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for item in wordlist:
      if match_with_gaps(my_word,item):
        print(item,end = ' ') 



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guess_num =6
    warning_num =3

    letters_guessed =[]

    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is',len(secret_word),'letters long.')
      
    while guess_num >0 and not is_word_guessed(secret_word,letters_guessed):
      is_warning = True
      is_wrong = True

      print('You have',guess_num,'guesses left')
      print(get_guessed_word(secret_word,letters_guessed))
      print(get_available_letters(letters_guessed))
      user_input = input('Please guess a letter:')

      if user_input.isalpha() or user_input=='*':
        if user_input =='*':
          is_wrong =False
          is_warning =False
          show_possible_matches(get_guessed_word(secret_word,letters_guessed))
        
        else:  
          if user_input not in letters_guessed:
            is_warning =False
            letters_guessed.append(user_input)
            if user_input in secret_word:
              is_wrong =False
              print('Good Guess')
      if is_warning:
        if user_input.isalpha():
          print('Already guessed that')
        else:
          print('Enter only characters')
        if warning_num:
          warning_num-=1
          print('You have',warning_num,'warnings left')
        else:
          guess_num-=1
        
      elif is_wrong:
        print('Wrong Guess')
        if user_input in 'aeouiy':
          guess_num-=2
        else:
          guess_num-=1

    if is_word_guessed(secret_word,letters_guessed):
    
      print("You won!")
    else:
      print('Word is:',secret_word)
    unique_str =''
    for item in secret_word:
      if item not in unique_str:
        unique_str+=item 
  
    print('Score:',guess_num*len(unique_str))



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
  

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
#   secret_word = choose_word(wordlist)
#    hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and 
# uncomment the following two lines. 

  secret_word = choose_word(wordlist)
  hangman_with_hints(secret_word)
