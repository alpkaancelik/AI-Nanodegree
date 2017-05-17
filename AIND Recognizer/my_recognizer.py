import warnings
from asl_data import SinglesData

def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Likelihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    # TODO implement the recognizer
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    # loop over each item in the test set
    for key in test_set.get_all_Xlengths():
        # An empty dictionary to store results
        predicted_words = {}

        # Getting the single item tuple for use with the hmmlearn library
        X_key, lengths_key = test_set.get_item_Xlengths(key)

        # loop over each word
        for word, model in models.items():
            try:
                predicted_words[word] = model.score(X_key, lengths_key)
            # If the hmmlearn library fails, we should save a very low number, so I assign negative infinity
            except: 
                predicted_words[word] = float("-inf")
                continue

        probabilities.append(predicted_words)
        guess = max(predicted_words, key = predicted_words.get)
        guesses.append(guess)        

    return probabilities, guesses