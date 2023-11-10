import json
import requests
import argparse


parser = argparse.ArgumentParser(description='Get specific rsID data from dbSNP')
parser.add_argument('-rs', '--rsid', required=True, type=str, help='Enter a valid rsID')
parser.add_argument('-f', '--file',  required=True, type=str, help='Enter a file name with .json')
args = parser.parse_args()

class GetData:

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def __init__(self, rsid, file):
        self.rsid = rsid
        self.file = file

    def fetch_data(self):
        request_url = f'{self.BASE_URL}efetch.fcgi?db=SNP&id={self.rsid}&rettype=json&retmode=text'
        response = requests.get(request_url)

        if response.status_code == 200:
            data = response.json()
            with open(self.file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            print('Please try again')
        


if __name__ == '__main__':
    get_file = GetData(args.rsid, args.file)
    get_file.fetch_data()