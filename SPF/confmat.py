'''
Module with BinaryConfusionMatrix class
'''

class BinaryConfusionMatrix:
    '''Class handling binary confusion matrix and it's evaluation'''

    def __init__(self, pos_tag, neg_tag):
        '''
        Params:
        pos_tag: label of positive value
        neg_tag: label of negative value
        '''
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag

        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0


    def as_dict(self):
        '''
        Returns dictionary with all parts of the confusion matrix
        Keys:
        (tp: true positive, tn: true negative, fp: false positive, fn: false negative)
        '''
        ret = dict()
        ret['tp'] = self.tp
        ret['tn'] = self.tn
        ret['fp'] = self.fp
        ret['fn'] = self.fn

        return ret


    def update(self, truth, prediction):
        '''
        Compare given pair and update confusion matrix accordingly
        Raises ValueError if given labels don't match this matrix's labels
        Params:
        truth - expected label
        prediction - predicted label
        '''
        if truth == self.pos_tag:
            if prediction == self.pos_tag:
                self.tp += 1
            elif prediction == self.neg_tag:
                self.fn += 1
            else:
                raise ValueError
        
        elif truth == self.neg_tag:
            if prediction == self.pos_tag:
                self.fp += 1
                return True
            elif prediction == self.neg_tag:
                self.tn += 1
            else:
                raise ValueError

        else:
            raise ValueError

        return False


    def compute_from_dicts(self, truth_dict, pred_dict):
        '''
        Compare labels from two dictionaries and compute their confusion matrix
        '''
        self.null_out_matrix()

        for key in pred_dict:
            if key in truth_dict:                
                if(self.update(truth_dict[key], pred_dict[key])):
                    print(key)
                    pass

    
    def null_out_matrix(self):
        self.tp, self.tn, self.fp, self.fn = 0, 0, 0, 0


if __name__ == '__main__':
    cm1 = BinaryConfusionMatrix(pos_tag=True, neg_tag=False)
    print(cm1.as_dict())
    cm1.update(True, True)
    print(cm1.as_dict())
    
    truth_dict = {'em1': 'SPAM', 'em2': 'SPAM', 'em3': 'OK', 'em4': 'OK'}
    pred_dict = {'em1': 'SPAM', 'em2': 'OK', 'em3': 'OK', 'em4': 'SPAM'}
    cm2 = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    cm2.compute_from_dicts(truth_dict, pred_dict)
    print(cm2.as_dict())
