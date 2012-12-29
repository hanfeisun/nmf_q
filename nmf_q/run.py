import numpy
from .io import *

class NMF_Run(object):
    def __init__(self, beds_table, mask_path, process_name, **args):
        self.beds = BedSet(beds_table)
        self.mask = Mask(mask_path)
        self.process_name = process_name
    def run(self):
        self.masked_matrix = self.beds.mask_by(self.mask)
        print "mask successfully"
        print "start running NMF.."
    def display(self):
        pass
    def clean(self):
        self.beds.delete_temp_files()
        self.mask.delete_temp_files()
        print "cleaned"


class Nimfa_NMF_Run(NMF_Run):
    def __init__(self, beds_table, mask_path,**args):
        NMF_Run.__init__(self, beds_table, mask_path,**args)
    def run(self):
        # TODO: estimate rank
        NMF_Run.run(self)
        import nimfa
        self.fctr = nimfa.mf(self.masked_matrix,
                             seed            = "nndsvd",
                             rank            = 10,
                             method          = "bmf",
                             max_iter        = 1000,
                             initialize_only = True,
                             lambda_w        = 1.1,
                             lambda_h        = 1.1)
        self.fctr_res = nimfa.mf_run(self.fctr)
