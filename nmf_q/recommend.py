from .io import Coef, Basis, Bed, Mask
from numpy.linalg import pinv
from numpy import correlate
from pprint import pprint
from scipy.stats import pearsonr
class NMF_Recommendation(object):
    def __init__(self, basis_path, coef_path, query_path, mask_path, query_name="query"):
        self.basis = Basis(basis_path)
        self.coef = Coef(coef_path)
        self.query = Bed(query_path, query_name)
        self.mask = Mask(mask_path)
    def load(self):
        self.query.mask_by(self.mask)
        self.masked_query = self.query.to_masked_array()
        self.basis.load()
        self.coef.load()
        self.inversed = pinv(self.basis.narray)
    def run(self):
        projection = self.inversed.dot(self.masked_query)
        result = []
        for i in range(self.coef.narray.shape[1]):
            result.append([self.coef.datasets[i],
                           pearsonr(self.coef.narray[:,i], projection)])
        pprint(projection)
        pprint(sorted(result, key=lambda x:x[1][0]))
