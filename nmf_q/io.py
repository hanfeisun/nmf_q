import numpy
import subprocess
import os
import sys

class NMF_Base(self):
    # global variable for all inherit
    def __init__(self):
        self.files = []
        self.temp_files = []
        self.tmp_file_counter = 0

    def create_temp_file(self, description):
        temp_file = "NMF_%s_%d_%d_%s" % (self.__class__.__name__,
                                         os.getpid(),
                                         self.tmp_file_counter,
                                         description)

        # Test whether the path is writable
        if not os.exists(temp_file):
            open(temp_file,'w').close()
            print "creating" + temp_file
        else:
            print "file already exists, exit"
            sys.exit(1)
        self.temp_files.append(temp_file)
        self.temp_file_counter += 1
        return self.temp_files

    def delete_temp_files(self):
        for a_file in self.temp_files:
            print "deleting" + a_file
            os.remove(a_file)

    def run_cmd (command):
        print "Run: %s" % command
        subprocess.call(command,shell=True)

    def count_lines(a_file):
        count = -1
        for count, line in enumerate(open(a_file)):
            pass
        return count + 1

class Beds(NMF_Base):
    def __init__(self, beds_table):
        NMF_Base.__init__(self)
        for line in open(beds_table):
            line = line.strip().split()
            if os.path.isfile(line[1]):
                self.beds.append({"name": line[0], "path": line[1]})
            else:
                self.missed_beds.append({"name": line[0], "path": line[1]})
                print "%s does not exist. Skipped" % line[0], line[1]
    @property
    def length(self):
        return len(self.beds)

    def mask_by(self,mask):
        self.masked_matrix = numpy.zeros((mask.length, self.length))
        self.mask = mask
        for bed_idx,bed in enumerate(self.beds):
            print "init", bed["name"], "bed file", bed["path"]
            temp_file = self.create_temp_file(bed["name"])
            self.run_cmd()
            for interval in open(temp_file):
                interval = interval.strip().split()
                mask_name = interval[0]
                self.mask_matrix[mask.idx_dict[mask_name],bed_idx] = 1
        return self.mask_matrix

class Mask(NMF_Base):
    def __init(self, mask_path, mask_format=""):
        # Future: implement mask_format

        NMF_Base.__init__(self)
        self.idx_dict = {}
        for idx, i in enumerate(open(mask_path)):
            mask_name = i.strip().split()[3]
            self.idx_dict[mask_name] = idx

    @property
    def length(self):
        return len(self.idx_dict)
