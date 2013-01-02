import numpy
import subprocess
import os
class NMF_Base(object):
    # global variable for all inherit
    def __init__(self, verbose=False):
        self.files = []
        self.temp_files = []
        self.temp_file_counter = 0
        self.verbose = verbose

    @staticmethod
    def try_touch(file_path):
        if not os.path.exists(file_path):
            open(file_path,'w').close()
            print "creating",file_path
        else:
            print "file already exists, skip" , file_path
            raise

    def create_persist_file(self, description):
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        persist_file = os.path.join(self.temp_dir,
                                    "p_NMF_%s_%d__%s" % (self.__class__.__name__,
                                                         os.getpid(),
                                                         description))
        NMF_Base.try_touch(persist_file)
        return persist_file

    @property
    def temp_dir(self):
        return "NMF_%d" % os.getpid()


    def create_temp_file(self, description):
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        temp_file = os.path.join(self.temp_dir,
                                 "NMF_%s_%d_%d_%s" % (self.__class__.__name__,
                                                      os.getpid(),
                                                      self.temp_file_counter,
                                                      description))
        # Test whether the path is writable
        self.try_touch(temp_file)
        self.temp_files.append(temp_file)
        self.temp_file_counter += 1
        return temp_file

    def delete_temp_files(self):
        for a_file in self.temp_files:
            if self.verbose:
                print "deleting",a_file
            try:
                os.remove(a_file)
                self.temp_file_counter -= 1
                del self.temp_files[self.temp_files.index(a_file)]
            except OSError:
                pass
        print "delete all temp files successfully"
    @staticmethod
    def run_cmd (command):
        print "Run: %s" % command
        subprocess.call(command,shell=True)
    @staticmethod
    def count_lines(a_file):
        count = -1
        for count, line in enumerate(open(a_file)):
            pass
        return count + 1
    def expand_path(self,path):
        return os.path.expanduser(path)

class Bed(NMF_Base):
    def __init__(self, path, name, description=""):
        NMF_Base.__init__(self,verbose=True)
        self.path = path
        self.name = name
        self.description = description
    def mask_by(self, mask):
        self.masked_result = self.create_temp_file(self.description)
        self.mask = mask
        NMF_Base.run_cmd("intersectBed -b %s -a %s -wa > %s"
                         % (self.path, self.mask.path, self.masked_result))
        return self.masked_result
    def to_masked_array(self):
        self.masked_matrix = numpy.zeros((self.mask.length))
        for interval in open(self.masked_result):
            interval = interval.strip().split()
            mask_name = interval[3]
            self.masked_matrix[self.mask.idx_dict[mask_name]] = 1.0
        return self.masked_matrix
    def clean(self):
        self.delete_temp_files()


class BedSet(NMF_Base):
    def __init__(self, beds_table):
        NMF_Base.__init__(self)
        self.beds = []
        self.missed_beds = []

        for line in open(beds_table):
            line = line.strip().split()
            if not line: continue

            bed = Bed(description = line[0],
                      name        =  line[1],
                      path        =  self.expand_path(line[2]))

            if os.path.isfile(bed.path):
                self.beds.append(bed)
            else:
                self.missed_beds.append(bed)
                print "{bed.name} | {bed.path} not found. Skipped".format(bed=bed)
    @property
    def length(self):
        return len(self.beds)

    def mask_by(self,mask):
        self.masked_matrix = numpy.zeros((mask.length, self.length))
        self.mask = mask
        for bed_idx,bed in enumerate(self.beds):
            print "init", bed.name, "bed file", bed.path
            temp_file = bed.mask_by(mask)
            for interval in open(temp_file):
                interval = interval.strip().split()
                mask_name = interval[3]
                self.masked_matrix[mask.idx_dict[mask_name],bed_idx] = 1.0
        print "The shape of masked matrix is",self.masked_matrix.shape
        return self.masked_matrix

    @property
    def mm_colnames(self, key="name"):
        return [i.description for i in self.beds]

    @property
    def mm_rownames(self):
        return self.mask.mask_name_list

class Mask(NMF_Base):
    def __init__(self, mask_path, mask_format=""):
        # Future: implement mask_format
        NMF_Base.__init__(self)
        self.idx_dict = {}
        self.mask_name_list = []
        self.path = mask_path
        for idx, i in enumerate(open(mask_path)):
            mask_name = i.strip().split()[3]
            self.mask_name_list.append(i.strip())
            self.idx_dict[mask_name] = idx

    @property
    def length(self):
        return len(self.idx_dict)


class Basis(NMF_Base):
    def __init__(self, base_path):
        # Future: implement mask_format
        NMF_Base.__init__(self)
        self.base_path = base_path
        self.feature_cnt = len(open(base_path).readline().strip().split("\t")) - 4
        # First 4 columns are not features
        self.site_cnt = NMF_Base.count_lines(base_path) - 1

    def load(self):
        with open(self.base_path) as bf:
            self.features = bf.readline().strip().split("\t")[4:]
            self.narray = numpy.zeros((self.site_cnt, self.feature_cnt))
            self.sites = []
            for idx,i in enumerate(bf):
                if idx % 100000 == 0:
                    print "loading basis matrix: progress %d/%d" %(idx, self.site_cnt)
                i = i.strip().split()
                if i:
                    self.sites.append(i[:4])
                    self.narray[idx,:] = map(float,i[4:])
        return self.narray


class Coef(NMF_Base):
    def __init__(self, coef_path):
        NMF_Base.__init__(self)
        self.coef_path = coef_path
        self.feature_cnt = NMF_Base.count_lines(coef_path) - 1
        self.dataset_cnt = len(open(coef_path).readline().strip().split())
    def load(self):
        print "loading coef matrix.."
        with open(self.coef_path) as cf:
            self.datasets = cf.readline().strip().split()
            self.features = []
            self.narray = numpy.zeros((self.feature_cnt, self.dataset_cnt))
            for idx,i in enumerate(cf):
                i = i.strip().split()
                if i:
                    self.features.append(i[0])
                    self.narray[idx,:] = map(float,i[1:])
        return self.narray
