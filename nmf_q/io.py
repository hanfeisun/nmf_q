import numpy
import subprocess
import os
import sys

class NMF_Base(object):
    # global variable for all inherit
    def __init__(self, verbose=False):
        self.files = []
        self.temp_files = []
        self.temp_file_counter = 0
        self.verbose = verbose

    def create_temp_file(self, description):
        temp_file = "NMF_%s_%d_%d_%s" % (self.__class__.__name__,
                                         os.getpid(),
                                         self.temp_file_counter,
                                         description)
        # Test whether the path is writable
        if not os.path.exists(temp_file):
            open(temp_file,'w').close()
            print "creating",temp_file
        else:
            print "file already exists, exit"
            sys.exit(1)
        self.temp_files.append(temp_file)
        self.temp_file_counter += 1
        return temp_file

    def delete_temp_files(self):
        for a_file in self.temp_files:
            if self.verbose:
                print "deleting",a_file
            os.remove(a_file)
            self.temp_file_counter -= 1
        print "delete all temp files successfully"
    @staticmethod
    def run_cmd (command):
        print "Run: %s" % command
        subprocess.call(command,shell=True)

    def count_lines(a_file):
        count = -1
        for count, line in enumerate(open(a_file)):
            pass
        return count + 1
    def expand_path(self,path):
        return os.path.expanduser(path)

class Beds(NMF_Base):
    def __init__(self, beds_table):
        NMF_Base.__init__(self)
        self.beds = []
        self.missed_beds = []

        for line in open(beds_table):
            line = line.strip().split()
            if not line: continue

            bed = {"desc": line[0],
                   "name": line[1],
                   "path": self.expand_path(line[2])}

            if os.path.isfile(bed["path"]):
                self.beds.append(bed)
            else:
                self.missed_beds.append(bed)
                print "{name} | {path} not found. Skipped".format(**bed)
    @property
    def length(self):
        return len(self.beds)

    def mask_by(self,mask):
        self.masked_matrix = numpy.zeros((mask.length, self.length))
        self.mask = mask
        for bed_idx,bed in enumerate(self.beds):
            print "init", bed["name"], "bed file", bed["path"]
            temp_file = self.create_temp_file(bed["name"])
            NMF_Base.run_cmd("intersectBed -b %s -a %s -wa > %s"
                             % (bed["path"], self.mask.path, temp_file))
            for interval in open(temp_file):
                interval = interval.strip().split()
                mask_name = interval[3]
                self.masked_matrix[mask.idx_dict[mask_name],bed_idx] = 1.0
        print "The shape of masked matrix is",self.masked_matrix.shape
        return self.masked_matrix

    @property
    def masked_matrix_colnames(self, key="name"):
        return [i[key] for i in self.beds]

    @property
    def masked_matrix_rownames(self):
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
            self.mask_name_list.append(self.mask_name_list)
            self.idx_dict[mask_name] = idx

    @property
    def length(self):
        return len(self.idx_dict)
