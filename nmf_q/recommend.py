from .io import Coef, Basis, Bed, Mask, BedSet
from numpy.linalg import pinv
from pprint import pprint
from scipy.spatial.distance import correlation
import time
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
            (method.__name__, args, kw, te-ts)
        return result

    return timed

class NMF_Recommendation(object):
    def __init__(self, basis_path, coef_path, mask_path):
        self.basis = Basis(basis_path)
        self.coef = Coef(coef_path)
        self.mask = Mask(mask_path)
        self.basis.load()
        self.coef.load()
        self.inversed = pinv(self.basis.narray)

    def process_query(self, query_path, query_description="query"):
        self.query_description = query_description
        self.query = Bed(query_path, query_description, query_description)
        self.query.mask_by(self.mask)
        self.masked_query = self.query.to_masked_array()
        self.query.clean()
        self.projection = self.inversed.dot(self.masked_query)


    def find_similarity(self, similar_func = correlation):
        self.result = []
        for i in range(self.coef.narray.shape[1]):
            self.result.append([self.coef.datasets[i],
                           similar_func(self.coef.narray[:,i],
                                        self.projection)])
        self.result = sorted(self.result, key=lambda x:x[1])

    def evaluate_result(self, expected=""):
        if not expected:
            e = self.query_description
        else:
            e = expected
        for idx,a_similarity in enumerate(self.result):
            if a_similarity[0] == e:
                return {"expected":e,
                        "rank": idx,
                        "top_5": self.result[:5],}

        raise
    def _pipe(self, query_path, query_description, similar_func):
        self.process_query(query_path, query_description)
        self.find_similarity(similar_func)
        return self.evaluate_result()



class NMF_Recommendation_Set(object):
    def __init__(self, basis_path, coef_path, mask_path):
        self.rec = NMF_Recommendation(basis_path, coef_path, mask_path)
    def query_set(self, querys_table,similar_func=correlation):
        q = BedSet(querys_table)
        evaluate_list = []
        for a_bed in q.beds:
            evaluate_list.append(self.rec._pipe(query_path = a_bed.path,
                                                query_description = a_bed.description,
                                                similar_func=similar_func))
        cost_sum = sum([i["rank"] for i in evaluate_list])

        return evaluate_list, cost_sum
