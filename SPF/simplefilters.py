from basefilter import Basefilter
import random

class NaiveFilter(Basefilter):

    def train_email(self, filename, body, truth):
        pass

    def eval_email(self, filename, body):
        return 'OK'


class ParanoidFilter(Basefilter):

    def train_email(self, filename, body, truth):
        pass

    def eval_email(self, filename, body):
        return 'SPAM'


class RandomFilter(Basefilter):

    def train_email(self, filename, body, truth):
        pass

    def eval_email(self, filename, body):
        return random.choice(['SPAM', 'OK'])


if __name__ == '__main__':

    data_path = 'SPF/data/2'
    import quality
    from filter import MyFilter
    rf = RandomFilter()
    pf = ParanoidFilter()
    nf = NaiveFilter()
    mf = MyFilter()

    rf.test(data_path)
    rq = quality.compute_quality_for_corpus(data_path)

    pf.test(data_path)
    pq = quality.compute_quality_for_corpus(data_path)

    nf.test(data_path)
    nq =quality.compute_quality_for_corpus(data_path)

    mf.test(data_path)
    mq =quality.compute_quality_for_corpus(data_path)

    print("Random quality:", rq)
    print("Paranoid quality:", pq)
    print("Naive quality:", nq)
    print("MyFilter quality:", mq)
    

