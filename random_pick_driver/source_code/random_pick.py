import os
import gzip
import random
import argparse
import shutil


command = argparse.ArgumentParser(description='Enter a VCF file: ')
command.add_argument('-f', '--file', required=True, type=str, help='Enter a a file name')
args = command.parse_args()

class PickWithRandom():

    def __init__(self, in_vcf: str, out_vcf: str):
        self.in_vcf = in_vcf
        self.out_vcf = out_vcf
        self.out_fh = open(out_vcf, 'w')
        if in_vcf.endswith('.gz'):
            self.in_fh = gzip.open(in_vcf, 'rt')
        else:
            self.in_fh = open(in_vcf, 'r')

    def pick_row(self):

        out_compressed_vcf = 'render_completed_test_data.vcf.gz'
        range_of_sampling_numbers = 999

        random.seed(1)

        for line in self.in_fh:
            if line.startswith('#'):
                self.out_fh.write(line)
            else:
                r = random.randint(0, range_of_sampling_numbers)
                if r == 0:
                    self.out_fh.write(line)

        self.in_fh.close()
        self.out_fh.close()


        with open(self.out_vcf, 'rb') as f_in:
            with gzip.open(out_compressed_vcf, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(self.out_vcf)

if __name__ == '__main__':
    sampling = PickWithRandom(args.file, 'temp.vcf')
    sampling.pick_row()
