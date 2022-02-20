from collections import Counter
import math
from os import DirEntry, listdir

from basefilter import Basefilter
from procemail import ProcessedEmail

DIVIDER_VALUE = 5     #e-mails with eval. value greater DIVIDER_VALUE => SPAM

class MyFilter(Basefilter):
    '''Class which decides whether an email is spam or ham'''

    def __init__(self):
        '''MyFilter class constructor'''
        #initialize properties for important data
        super().__init__()
        self.ham_tokens = Counter()
        self.ham_count = 0
        self.spam_tokens = Counter()
        self.spam_count = 0

        self.divider_value = DIVIDER_VALUE

        #dictionaries for processed data -> word probabilities
        self.token_spam_prob = dict()
        self.token_ham_prob = dict()

        #load precalculated data if available
        self.load_prepared_data()
        self.calculate_token_probabilities()


    def train(self, dir_path):
        '''
        Trains module on given corpus and processes the results
        Params:
        dir_path: Path and name of the corpus
        '''        
        truth_list = super().train(dir_path)
        self.calculate_token_probabilities()
        #self.determine_divider(truth_list)

    
    def determine_divider(self, truth_list):
        '''
        Fits divider value to fit latest loaded training set
        Params:
        truth_list - dictionary containing correct labels of messages
        '''
        div_val = 0
        false_count = 0

        for name, body in self.corpus.emails():
            prob = self.calculate_prob_spam(name, body)
            if(prob > self.divider_value):
                if(truth_list[name] == 'OK'):
                    div_val += 10 * (prob - self.divider_value)
                    false_count += 10
            else:
                if(truth_list[name] == 'SPAM'):
                    div_val += prob - self.divider_value
                    false_count += 1

        if(false_count > 0):
            self.divider_value += div_val / false_count
        print('\n', self.divider_value)


    def train_email(self, filename, body, truth):
        '''
        Processes individual email file for training purposes
        Params:
        filename: Name of the emails file
        body: Text of the email file
        truth: The correct label of the email
        '''
        #class ProcessedEmail extract valuable information 
        # from email body in constructor
        pe = ProcessedEmail(filename, body, truth)
        if truth == 'OK':
            self.ham_count += 1
            self.ham_tokens += pe.get_normalized_counter()          
        elif truth == 'SPAM':
            self.spam_count += 1
            self.spam_tokens += pe.get_normalized_counter()


    def calculate_token_probabilities(self):
        '''
        Calculates probabilities for individual words being in a spam/ham
        '''
        self.token_spam_prob = dict()
        self.token_ham_prob = dict()
        all_tokens = self.spam_tokens + self.ham_tokens

        for t in all_tokens:
            prob_ts = self.spam_tokens[t] / self.spam_count            
            prob_th = self.ham_tokens[t] / self.ham_count

            #Prevent zero division exception later if probability is zero
            if prob_ts == 0:
                prob_ts = 0.01 * all_tokens[t] / len(all_tokens)

            if prob_th == 0:
                prob_th = 0.01 * all_tokens[t] / len(all_tokens)
            
            #Save probabilities for this word
            self.token_spam_prob[t] = prob_ts
            self.token_ham_prob[t] = prob_th


    def eval_email(self, filename, body):
        '''
        Calls calculate_prob_spam for given email and then predicts correct label
        Params:
        filename: name of the evaluated email's file
        body: text of the email's file
        '''
        prob_spam_ln = self.calculate_prob_spam(filename, body)
        
        #assign label
        if prob_spam_ln > self.divider_value:
            return 'SPAM'
        else:
            return 'OK'


    def calculate_prob_spam(self, filename, body):
        '''
        Returns representation of probability that given email
        is SPAM based on trained data (token probabilities).
        Params:
        filename: name of the evaluated email's file
        body: text of the email's file
        '''
        #extract valuable info from body text
        pe = ProcessedEmail(filename, body)

        #probabilities of any email being spam or ham
        p_s = self.spam_count / (self.ham_count + self.spam_count)
        p_h = self.ham_count / (self.ham_count + self.spam_count)

        #number representing probability of this email being spam (but not <0;1>)
        #prob_spam_ln = math.log(p_s/p_h)
        prob_spam_ln = 0

        #for every word in evaluated email
        for t in pe.get_normalized_counter():
            #ignore unseen words in evaluation
            if t not in self.token_spam_prob:
                continue

            #account every word's probability in email's probability
            prob_spam_ln += math.log(self.token_spam_prob[t] / self.token_ham_prob[t])
        
        return prob_spam_ln


    def save_prepared_data(self, min_appearance = None):
        '''
        Saves extracted token data to files so it doesn't have to be trained again
        Save only words which were counted in more than 'min_appearance' emails
        Params: 
        min_appearance: (default: 1) minimal number of emails 
            the word have to appear in to be saved
        '''
        if min_appearance == None:
            min_appearance = 1

        #HAM tokens information and number of HAMs
        with open('preham.txt', mode='w', encoding='utf-8') as f:
            #total number of HAM emails on first row
            f.write(f'{self.ham_count}\n')

            #line for each token and number of SPAMs it appeared in
            for t in self.ham_tokens:
                if self.ham_tokens[t] >= min_appearance:
                    f.write(f'{t} {self.ham_tokens[t]}\n')

        #SPAM tokens information and sumber of SPAMs
        with open('prespam.txt', mode='w', encoding='utf-8') as f:
            #total number of SPAM emails on first row
            f.write(f'{self.spam_count}\n')

            #line for each token and number of SPAMs it appeared in
            for t in self.spam_tokens:
                if self.spam_tokens[t] >= min_appearance:
                    f.write(f'{t} {self.spam_tokens[t]}\n')


    def load_prepared_data(self):
        '''
        Loads extracted token data from files, if they exist
        '''
        #Check if both data files exist
        if 'preham.txt' not in listdir() or 'prespam.txt' not in listdir():
            #if not set spam and ham count to zero to prevent zero division error
            self.ham_count = 1
            self.spam_count = 1
            return

        #Save HAM token information file
        with open('preham.txt', mode='r', encoding='utf-8') as f:
            #number of HAM emails in the first line
            self.ham_count = int(f.readline())

            #save one token and it's HAM appearence count in each line
            for line in f:
                line_split = line.rstrip().split(' ')
                self.ham_tokens[line_split[0]] = int(line_split[1])

        #Save SPAM token information file
        with open('prespam.txt', mode='r', encoding='utf-8') as f:
            #number of SPAM emails in the first row
            self.spam_count = int(f.readline())

            #token and it's SPAM appearance count in each line
            for line in f:
                line_split = line.rstrip().split(' ')
                self.spam_tokens[line_split[0]] = int(line_split[1])
