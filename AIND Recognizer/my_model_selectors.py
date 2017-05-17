import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences

from sklearn.model_selection import KFold

class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """
    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        best_score = float("Inf")
        final_model = None

        for num_states in range(self.min_n_components, self.max_n_components+1):

            try:
                #run the model using hmmlearn library, score it, and calculate the BIC
                model =  GaussianHMM(n_components=num_states, n_iter=1000).fit(self.X, self.lengths)
                logL = model.score(self.X, self.lengths)
                parameters = num_states * num_states + 2 * num_states * len(self.X[0]) - 1
                bic = (-2) * logL + np.log(len(self.X)) * parameters

                #choose the best model we have so far
                if  bic < best_score:
                    best_score = bic
                    final_model = model
            
            except:
                pass

        return final_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        dic_array=[]
        results={}
        other_results ={}
        dic = []

        try:
            model=None
            for num_states in range(self.min_n_components,self.max_n_components+1):
                otherLogL = 0.0
                counter = 0

                # Fitting and scoring the model
                model = GaussianHMM(n_components=num_states, n_iter=1000).fit(self.X, self.lengths)
                logL = model.score(self.X, self.lengths)

                #Skipping the current word             
                for word in self.hwords:
                    if word == self.this_word:
                        continue
                    X, lengths = self.hwords[word]
                    otherLogL += model.score(X, lengths)
                    counter += 1

                #Updating the result dictionaries with the scores above
                otherLogL /= float(counter)
                results[num_states] = logL
                other_results[num_states] = otherLogL

                #Calculate and record the DIC
                dic = results[num_states] -  other_results[num_states]
                dic_array.append((model,dic))
        except:
            pass
        if dic == []:
            return None

        return max(dic_array, key= lambda x: x[1])[0]


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        logs_array = []
        best_score = -float("Inf")
        best_model = None

        for num_states in range(self.min_n_components, self.max_n_components+1):

            try:
                split_method = KFold(n_splits=min(3, len(self.sequences)))

                #Doing crossvalidation and fitting the model accordingly
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                        X_train, lengths_train = combine_sequences(cv_train_idx, self.sequences)
                        X_test, lengths_test = combine_sequences(cv_test_idx, self.sequences)
                        model =  GaussianHMM(n_components=num_states, n_iter=1000).fit(X_train, lengths_train)
                        logL = model.score(X_test, lengths_test)
                        logs_array.append(logL)
                mean_score = np.mean(logs_array)

                #Update the best model
                if  mean_score > best_score:
                    best_score = mean_score
                    best_model = model        
            
            except:
                pass

        return best_model