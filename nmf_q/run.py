import numpy
import nimfa
from .io import *

class NMF_Run(object):
    def __init__(self, beds, mask):
        NMF_Base.__init__(self)
        self.beds = Beds(beds)
        self.mask = Mask(mask)
    def run(self):
        masked_matrix = self.beds.mask_by(self.mask)
        self.fctr = nimfa.mf(masked_matrix,
                             seed            = "nndsvd",
                             rank            = 10, # TODO
                             method          = bmf,
                             max_iter        = 50,
                             initialize_only = True,
                             lambda_w        = 1.1,
                             lambda_h        = 1.1)
        self.fctr_res = nimfa.mf_run(fctr)
