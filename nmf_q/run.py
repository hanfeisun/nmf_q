import numpy
import pymf
from .io import *

class NMF_Run(object):
    def __init__(self, beds_table, mask_path, process_name, **args):
        self.beds = Beds(beds_table)
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
    def __init__(self, beds_table, mask_path):
        NMF_Run.__init__(self, beds_table, mask_path)
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

class Pymf_NMF_Run(NMF_Run):
    def __init__(self, **args):
        NMF_Run.__init__(self, **args)
        self.output_W_name = self.process_name+".W"
        self.output_H_name = self.process_name+".H"
        self.rank = 10
    @property
    def masked_array(self):
        return numpy.array(self.masked_matrix)

    def run(self):
        NMF_Run.run(self)
        from pymf.bnmf import BNMF
        self.bnmf_mdl = BNMF(data             = self.masked_array,
                             num_bases        = self.rank)
        self.bnmf_mdl.factorize(niter         =1000,
                                show_progress =True)
    def display(self):
        print self.bnmf_mdl.W
        print self.bnmf_mdl.H
    @property
    def W(self):
        return self.bnmf_mdl.W

    @property
    def H(self):
        return self.bnmf_mdl.H
    def output_matrix(self):
        print "outputing matrix W and H..."
        numpy.savetxt(self.output_W_name, self.bnmf_mdl.W, fmt="%.2e")
        numpy.savetxt(self.output_H_name, self.bnmf_mdl.H, fmt="%.2e")

    def output_metasites(self):
        for column in range(self.rank):
            print self.H[:,column] > 0.5

    def output_metasamples(self):
        pass
