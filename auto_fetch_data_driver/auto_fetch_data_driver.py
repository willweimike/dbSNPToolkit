import subprocess
import argparse

command = argparse.ArgumentParser()
command.add_argument('-in', '--inrs', required=True)
command.add_argument('-out', '--outfile', required=True)
args = command.parse_args()


class Autofetch:
    def __init__(self, inrs, outfile):
        self.inrs = inrs
        self.outfile = outfile
    
    def main(self):
        rs = self.inrs
        f = self.outfile
        cmd = f'python3 ./source_code/auto_fetch_data.py -rs {rs} -f {f}'
        subprocess.check_call(cmd, shell=True)


if __name__ == '__main__':
    Autofetch(args.inrs, args.outfile).main()
