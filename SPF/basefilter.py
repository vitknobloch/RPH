import os
import corpus as corpus_module
import utils

class Basefilter:
    '''
    Parent class to spam filter classes, unusable without further implementation
    Methods train_email and eval_email have to be implemented in children
    '''
    def __init__(self):
        '''BaseFilter class constructor'''
        self.corpus = None


    def train(self, dir_path):
        '''
        Gets every email and it's correct label and calls train_email function
        Params:
        dir_path: path to training corpus (directory)
        '''               
        #load correct lables
        truth_list = utils.read_classification_from_file(os.path.join(dir_path, '!truth.txt'))
        

        #call train_email
        self.corpus = corpus_module.Corpus(dir_path)
        for n, b in self.corpus.emails():
            self.train_email(n, b, truth_list[n])

        return truth_list


    def train_email(self, filename, body, truth):
        '''
        Function that processes each email for training
        HAS TO BE IMPLEMENTED IN CHILD CLASSES
        '''
        raise NotImplementedError


    def test(self, dir_path): 
        '''
        Calls test_dict to get preedicted labels dict and saves prediction to file
        Params:
        dir_path: path to testing corpus (directory)
        '''       
        pred_dict = self.test_dict(dir_path)
        utils.write_classification_to_file(pred_dict, os.path.join(dir_path, '!prediction.txt'))

    
    def test_dict(self, dir_path):
        '''
        Calls eval_email for every email in test corpus and return dictionary with labels
        Params:
        dir_path: path to testing corpus (directory)
        '''
        if self.corpus == None:
            self.corpus = corpus_module.Corpus(dir_path)
        else:
            self.corpus.directory = dir_path

        pred_dict = dict()

        for name, body in self.corpus.emails():
            pred_dict[name] = self.eval_email(name, body)

        return pred_dict


    def eval_email(self, filename, body):
        '''
        Returns label prediction for email passed  in arguments
        HAS TO BE IMPLEMENTED IN CHILD CLASSES
        '''
        raise NotImplementedError
