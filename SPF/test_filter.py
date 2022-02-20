from filter import MyFilter
import quality
import os
from time import time


def test_training(training_corpuses, testing_corpus):
    print('\nTEST TRAINING:')
    time_start = time()
    mf = MyFilter()
    
    for corp in training_corpuses:
        print(f'  Training on {corp}...', end=" ")
        time_corp_start = time()
        mf.train(corp)
        print(f'{int((time() - time_corp_start)*1000)} ms')


    print('  Saving trained data...')
    mf.save_prepared_data()
    
    print(f'  Trained on {mf.spam_count + mf.ham_count} emails -' + 
        f'{100 * mf.spam_count / (mf.spam_count + mf.ham_count): .02f}% spam')
    print(f'  Testing on {testing_corpus}...')
    mf.test(testing_corpus)
    print(f'Test Complete - {int((time() - time_start)*1000)} ms')
    tst_print_quality(testing_corpus)


def test_loading(testing_corpus):
    print('\nTEST LOADING:')
    time_start = time()
    mf = MyFilter()

    print("  Loaing trained data...")    

    print(f'  Trained on {mf.spam_count + mf.ham_count} emails -' + 
        f'{100 * mf.spam_count / (mf.spam_count + mf.ham_count): .02f}% spam')
    print(f'  Testing on {testing_corpus}...')
    mf.test(testing_corpus)
    print(f'Test Complete - {int((time() - time_start)*1000)} ms')
    tst_print_quality(testing_corpus)
    


def tst_remove_prepared():
    try:
        os.remove('preham.txt')
        os.remove('prespam.txt')
    except:
        print('Removing prepared data failed')

def tst_print_quality(testing_corpus):
    quality_val, eval_dict = quality.compute_quality_for_corpus_with_stats(testing_corpus)
    email_count = sum(eval_dict[i] for i in eval_dict)
    correct_count = eval_dict['tp'] + eval_dict['tn']

    print('  Total emails evaluated:', email_count)
    print(f'  Correctly evaluated:    {correct_count} -{correct_count/email_count*100: .02f}%')
    print(f'  Incorrectly evaluated:  {eval_dict["fp"] + eval_dict["fn"]} (fp: {eval_dict["fp"]}, fn: {eval_dict["fn"]})') 
    print(f'Quality:{quality_val*100: .02f}')


if __name__ == '__main__':
    testing_corpus = 'data/2'
    training_corpuses = ['data/4', 'data/3', 'data/1']
    tst_remove_prepared()
    test_loading(testing_corpus)
    test_training(training_corpuses, testing_corpus)
    test_loading(testing_corpus)

