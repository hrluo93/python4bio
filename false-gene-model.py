import re
from Bio import SeqIO
import argparse

# ArgumentParser
parser = argparse.ArgumentParser(description='Search false gene model in the longest protein Sequences from gffread.')
parser.add_argument('-i', '--input', required=True, help='Input fasta file')
parser.add_argument('-o', '--output', required=True, help='Output file')

args = parser.parse_args()

# Open input
with open(args.input, 'r') as file:
    # Def output
    with open(args.output, 'w') as outfile:
        for record in SeqIO.parse(file, 'fasta'):
            # Search false protein Sequences
            if re.search(r'[A-Za-z]+\.[A-Za-z]+', str(record.seq)):
                # Output file table
                outfile.write(f"ID: {record.id}, Sequence: {record.seq}\n")