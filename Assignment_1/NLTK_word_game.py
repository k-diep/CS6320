import sys
import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Run this line in the terminal (Windows):
# python NLTK_word_game.py anat19.txt

# Try to get the file name from the first system line argument, and handle error cases
# Note: Currently ignoring all other system line arguments except for the first
try:
    file_name = sys.argv[1]

# Case when there are no system line argument
except IndexError:
    print("Add the file name as the first system line argument.")
    # Exit the program
    sys.exit(1)

# Catch all other errors
except Exception as e:
    print(e)
    # Exit the program
    sys.exit(1)

# print(file_name)

# Attempt to open the file (file_name is from the first argument)
try:
    with open(file_name, 'r') as file:
        raw_text = file.read()

# Catch if file could not be found
except FileNotFoundError:
    print("The file, ", file_name, ", cannot be found")
    sys.exit(1)

# Catch all other errors
except Exception as e:
    print(e)
    # Exit the program
    sys.exit(1)

# Print the first 1000 characters of raw_text
# print(raw_text[:1000])

# Tokenize the raw text
tokenized_raw_text = word_tokenize(raw_text)

# Display the first 10 tokens
print("The first 10 tokens:")
print(tokenized_raw_text[:10])

# Lexical diversity code adapted from https://github.com/kjmazidi/NLP/blob/master/Part_2-Words/Chapter_05_words/5.1_Words1.ipynb

# Finding the total number of tokens
print("\nThe number of tokens in %s: " % file_name, len(tokenized_raw_text))

# Finding the total number of unique tokens
unique_tokens = set(tokenized_raw_text)
print("The number of unique tokens in %s: " % file_name, len(unique_tokens))

# Printing the first 5 unique tokens
# print("The first 5 unique tokens in %s: " % file_name, list(unique_tokens)[:5])

# Calculating lexical diversity
print("Lexical diversity of %s: %.2f" % (file_name, (len(unique_tokens) / len(tokenized_raw_text))))

def preprocess_text(raw_text):

  # Tokenize the raw text and lowercase
  tokenized_raw_text = word_tokenize(raw_text.lower())
  # print(tokenized_raw_text)

  # Filter out tokens to tokens that are alpha
  alpha_tokens = [token for token in tokenized_raw_text if token.isalpha()]
  # print(alpha_tokens)

  # Filter out tokens to tokens that not in the in the stopword list
  stopwords_tokens = [token for token in alpha_tokens if token not in stopwords.words('english')]
  # print(stopwords_tokens)

  # Filter out tokens to tokens with a length > 5
  length_greater_than_5_tokens = [token for token in stopwords_tokens if len(token) > 5]
  # print(length_greater_than_5_tokens)

  # Lemmatize the tokens
  lemmatizer = WordNetLemmatizer()
  lemmatized_tokens = [lemmatizer.lemmatize(token) for token in length_greater_than_5_tokens]
  # print(lemmatized_tokens)

  # Create a set to get unique lemmas
  unique_lemmatized_tokens = set(lemmatized_tokens)
  # print(unique_lemmatized_tokens)
  # print(len(unique_lemmatized_tokens))

  # Do POS tagging on the unique lemmas
  tags = pos_tag(unique_lemmatized_tokens)
  print("\nThe first 20 words and their tag:")
  print("word : tag")
  print("----------------------------------------------------")
  for tag in tags[:20]:
    words, POS_tags = tag
    print(words, ":", POS_tags)

  # Note: After some light testing the number of nouns slightly differ after every run.
  # Filter the unique lemmas to only nouns to a list
  nouns = [word for word, tag in tags if tag.startswith("NN")]

  # Printing the number of non unique tokens from step a.
  print("\nNumber of tokens that are alpha, not in the NLTK stopword list, and have length > 5: ", len(length_greater_than_5_tokens))

  # Printing the number of nouns.
  print("Number of nouns: ", len(nouns), "\n")

  # Misunderstanding of the instructions - Scrapped this code
  # --------------------------------------------------------------
  # Get a random non unique token
  # random_non_unique_token = random.choice(length_greater_than_5_tokens)
  # print(random_non_unique_token)

  # Get the first random noun
  # random_noun_1 = random.choice(nouns)
  # print(random_noun_1)

  # Get the second random noun
  # random_noun_2 = random.choice(nouns)
  # print(random_noun_2)
  # --------------------------------------------------------------

  # Return list of non unique tokens, and list of nouns
  return length_greater_than_5_tokens, nouns

tokens, nouns = preprocess_text(raw_text)

# Creating a dictionary of {noun: count of noun}
noun_count_dictionary = {noun: tokens.count(noun) for noun in nouns}
# print(noun_count_dictionary)

# Adapted this code to sort https://www.geeksforgeeks.org/different-ways-of-sorting-dictionary-by-values-and-reverse-sorting-by-values/#
# Sorting the noun dict
noun_count_sorted = sorted(noun_count_dictionary.items(), key = lambda kv: kv[1], reverse=True)
# print(noun_count_sorted)

# Initialized the list of nouns
nouns_list = []

# Printing the 50 most common words and their counts
print("50 most common words and their counts in %s" % file_name)
print("noun : count")
print("----------------------------------------------------")
for key_value in noun_count_sorted[:50]:

  # Extract the noun, count from the tuple (key_value)
  common_noun, common_noun_count = key_value

  # Print the sorted nouns and their counts
  print(common_noun, ":", common_noun_count)
  nouns_list.append(common_noun)

# Function Definition: Print word with spaces in between
def print_word_with_spaces(word):
  for letter in word:
    print(letter, "", end='')


# Function of an instance of the word guessing game
def word_game(nouns_list, initial_points):

  # Choose a random noun in the nouns_list
  random_noun = random.choice(nouns_list)

  # Uncomment the next line to see the random noun
  # print("Random Noun: ", random_noun)

  # Initial Points
  points = initial_points

  # Create the initial current guessed word (which is _ * length of the word)
  current_guessed_word = []
  for i in range(len(random_noun)):
    current_guessed_word.append("_")

  print_word_with_spaces(current_guessed_word)

  # Guessing part of the game
  while(1):
    # Check to see if the user has won and return if so
    if '_' not in current_guessed_word:
      print("\nCongrats. You've guessed the word with", points, "points left.")
      return points

    else:
      # Ask the user for a letter
      user_letter = input("\nGuess a letter (enter \'!\' to exit): ")
      user_letter = user_letter.lower()

      # Checking if the input is "!" and exiting if it is
      if user_letter == "!":
        print("You had", points, "points left.")
        print("Exiting now.")
        sys.exit(0)

      # Checking if the input is an alpha char with size 1 (one letter)
      elif not user_letter.isalpha() or len(user_letter)!=1:
        print("\nPlease input one letter character.\nScore is", points)

      # Checking if user has already guessed that letter
      elif user_letter in current_guessed_word:
        print("\nYou already guessed that letter. Try again.\nScore is", points)

      # Checking if letter is in the random noun
      elif user_letter in random_noun:
        points += 1
        print("\nRight!\nScore is", points)

        # Replacing current_guessed_word with the current guess letter
        for letter_index in range(len(random_noun)):
          if random_noun[letter_index] == user_letter:
            current_guessed_word[letter_index] = random_noun[letter_index]

        # print(current_guessed_word)

      elif points < 1:
        print_word_with_spaces(current_guessed_word)
        print("\nGAME OVER, you ran out of points. The word was \"%s\"." % random_noun)
        sys.exit(0)

      else:
        points -= 1
        print("Sorry, guess again. Score is", points)

      # Print the current word
      print_word_with_spaces(current_guessed_word)

# Driver for the word guessing game
# Prompt user if they still want to play

# Current Points
points = 5
while(1):
  points_after_game = word_game(nouns_list, points)
  points = points_after_game