import numpy
import nimfa
from .io import *

class NMF_Run(object):
    def __init__(self, beds_table, mask_path):
        self.beds = Beds(beds_table)
        self.mask = Mask(mask_path)
    def run(self):
        # TODO: estimate rank
        masked_matrix = self.beds.mask_by(self.mask)
        self.fctr = nimfa.mf(masked_matrix,
                             seed            = "nndsvd",
                             rank            = 10,
                             method          = bmf,
                             max_iter        = 50,
                             initialize_only = True,
                             lambda_w        = 1.1,
                             lambda_h        = 1.1)
        self.fctr_res = nimfa.mf_run(fctr)
