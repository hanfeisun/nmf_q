import numpy
from .io import *

class NMF_Run(NMF_Base):
    def __init__(self, beds_table, mask_path, process_name, nmf_rank, max_iter, **args):
        NMF_Base.__init__(self)
        self.a = args
        self.beds = BedSet(beds_table)
        self.mask = Mask(mask_path)
        self.process_name = process_name
        self.preprocessed = False
        self.nmf_rank = nmf_rank
        self.max_iter = max_iter

    def mask_bed(self):
        self.masked_matrix = self.beds.mask_by(self.mask)
        print "mask successfully"

    def run(self):
        print "start running NMF.."

    def persist(self):
        self.output_metasites()
        self.output_metasamples()

    def output_metasamples(self):
        pass

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
        self.mask_bed()
        NMF_Run.run(self)
        import nimfa
        print repr(self.masked_matrix)
        print repr(self.masked_matrix.shape)
        self.fctr = nimfa.mf(numpy.matrix(self.masked_matrix),
                             seed            = "nndsvd",
                             rank            = self.nmf_rank,
                             method          = "bmf",
                             max_iter        = self.max_iter,
                             initialize_only = True,
                             lambda_w        = 1.1,
                             lambda_h        = 1.1)
        self.fctr_res = nimfa.mf_run(self.fctr)
        print 'Rss: %5.4f' % self.fctr_res.fit.rss()
        print 'Evar: %5.4f' % self.fctr_res.fit.evar()
        print 'K-L divergence: %5.4f' % self.fctr_res.distance(metric = 'kl')
        print 'Sparseness, W: %5.4f, H: %5.4f' % self.fctr_res.fit.sparseness()
        print 'Iteration: %d' % self.fctr_res.n_iter
    def output_metasites(self):
        for column in range(self.nmf_rank):
            metasite_file = self.create_persist_file("metasites_%d"%(column+1))
            # filter out masks whose intensity is zero
            filter_idx = numpy.nonzero(numpy.array(self.W[:,column]) > 0.1)[0]
            with open(metasite_file,"w") as mf:
                for row_idx in filter_idx:
                    mf.write("%s\t%.2e\n"%(self.beds.mm_rownames[row_idx],
                                           self.W[row_idx,column]))
        metasites_file = self.create_persist_file("metasites_all")
        with open(metasites_file,"w") as msf:
            # Header: the name of datasets
            msf.write("# chr\tstart\tend\tname\t"
                      +"\t".join(["Metasite_%d"%(i+1)
                                 for i in range(self.nmf_rank) ])
                      +"\n")


            fmt = "\t".join(["%.2e"]*self.nmf_rank) + "\n"
            for row_idx,row in enumerate(self.beds.mm_rownames):
                msf.write("%s\t"%self.beds.mm_rownames[row_idx])
                msf.write(fmt % tuple(numpy.array(self.W[row_idx,:])[0]))
    def output_metasamples(self):
        for row in range(self.beds.length):
            metasample_file = self.create_persist_file("metasample_%d_%s"
                                                       % (row+1,
                                                          self.beds.mm_colnames[row]))
            numpy.savetxt(fname = metasample_file,
                          X     = self.H[:,row],
                          fmt   = "%.2e")
        metasample_files = self.create_persist_file("metasample_all")
        with open(metasample_files,"w") as msf:
            # Header
            msf.write("\t".join(self.beds.mm_colnames)+"\n")
            fmt = "\t".join(["%.2e"]*self.beds.length) + "\n"

            for feature_idx in range(self.nmf_rank):
                msf.write("Feature_%d\t"%(feature_idx+1))
                msf.write(fmt % tuple(numpy.array(self.H[feature_idx,:])[0]))
    @property
    def W(self):
        return self.fctr_res.basis()

    @property
    def H(self):
        return self.fctr_res.coef()
