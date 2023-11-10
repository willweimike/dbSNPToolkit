import gzip
import json
import argparse
import pandas as pd
from typing import IO, Dict, Optional
from sqlalchemy import create_engine


command = argparse.ArgumentParser(description='Enter a VCF file: ')
command.add_argument('-f', '--file', required=True, type=str, help='Enter a a file name')
args = command.parse_args()

class VcfParser:

    header: str
    fh: IO
    VCF_KEYS = [
        'CHROM',
        'POS',
        'ID',
        'REF',
        'ALT',
        'QUAL',
        'FILTER',
        'INFO'
    ]

    def __init__(self, vcf: str):
        if vcf.endswith('.gz'):
            self.fh = gzip.open(vcf, 'rt')
        else:
            self.fh = open(vcf, 'r')
        self.set_header()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return

    def __iter__(self):
        return self

    def __next__(self):
        r = self.next()
        if r is not None:
            return r
        else:
            raise StopIteration

    def set_header(self):
        num_header_lines = 0
        for line in self.fh:
            if line.startswith('#'):
                num_header_lines += 1

        self.fh.seek(0)

        temp = []
        i = 0
        for line in self.fh:
            i += 1
            temp.append(line)
            if i == num_header_lines:
                break
        self.header = ''.join(temp)

    def next(self) -> Optional[Dict[str, str]]:
        line = self.fh.readline()

        if line == '':
            return None

        temp_lst = line.split('\t')

        count = 0
        assemble_lst = []
        for i in temp_lst:
            count += 1
            assemble_lst.append(i)
            if count == 8:
                break

        data_dict = dict(zip(self.VCF_KEYS, assemble_lst))

        for element in data_dict['INFO'].split(';'):
            if '=' in element:
                pos = element.index('=')
                key = element[0:pos]
                val = element[pos+1:]
            else:
                key, val = element, None
            data_dict[key] = val

        data_dict.pop('INFO')

        return data_dict

    def close(self):
        self.fh.close()


def extract_vcf_to_dataframe(vcf: str):

    collected_lst = []

    engine = create_engine('sqlite:///database.db')

    with VcfParser(vcf=vcf) as parser:
        for element in parser:
            collected_lst.append(element)

    df = pd.DataFrame(collected_lst)

    df.to_csv('output.csv', index=False)
    df.to_sql('vcf_data', engine, if_exists='append', index=False)

def extract_vcf_to_json(vcf: str):

    collected_lst = []

    with VcfParser(vcf=vcf) as parser:
        for element in parser:
            collected_lst.append(element)
        
    with open('output.json', 'w') as out_f:
        json.dump(collected_lst, out_f, indent=2)

if __name__ == '__main__':
    extract_vcf_to_dataframe(vcf=args.file)
    extract_vcf_to_json(vcf=args.file)
