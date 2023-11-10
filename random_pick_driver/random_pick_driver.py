import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--f_in', required=True)
args = parser.parse_args()

class Drive:

    def __init__(self, f_in):
        self.f_in = f_in

    def main(self):
        input = f'./data_files/{self.f_in}'
        cmd = f'python3 ./source_code/random_pick.py -f {input}'
        subprocess.check_call(cmd, shell=True)

if __name__ == '__main__':
    Drive(args.f_in).main()
