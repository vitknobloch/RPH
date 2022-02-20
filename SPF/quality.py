'''Module with functions to compute quality of a corpus with emails'''
import utils
import confmat


def quality_score(confusion_matrix_dict):
    '''
    Computes the quality value from confusion matrix
    Params:
    confusin_matrix_dict: dictionary with values from a confusion matrix
    '''
    tp = confusion_matrix_dict['tp']
    tn = confusion_matrix_dict['tn']
    fp = confusion_matrix_dict['fp']
    fn = confusion_matrix_dict['fn']

    return (tp + tn) / (tp + tn + 10*fp + fn)


def compute_quality_for_corpus(corpus_dir):
    '''
    Return float with value 0-1 describing the quality of given corpus
    Params:
    corpus_dir: path and name of the corpus directory
    '''
    score, eval_dict = compute_quality_for_corpus_with_stats(corpus_dir)
    return score


def compute_quality_for_corpus_with_stats(corpus_dir):
    '''
    Return float with value 0-1 describing the quality of given corpus
    and confusin matrix for fine-tuning purposes
    Params:
    corpus_dir: path and name of the corpus directory
    '''
    #load dictionaries
    truth_dict = utils.read_classification_from_file(
        f'{corpus_dir}/!truth.txt')
    pred_dict = utils.read_classification_from_file(
        f'{corpus_dir}/!prediction.txt')

    #compte confusion matrix
    bm = confmat.BinaryConfusionMatrix('SPAM', 'OK')
    bm.compute_from_dicts(truth_dict, pred_dict)
    eval_dict = bm.as_dict()

    return quality_score(eval_dict), eval_dict




if __name__ == '__main__':
    quality = compute_quality_for_corpus('data/1')
    print(quality)
    
