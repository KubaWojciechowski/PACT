import logging
import textwrap
import os
from typing import Tuple
from Bio import SeqIO
from pathlib import Path
import logging

from pact_core.utils import get_templates_path

class SequencePreprocessor():

    def __init__(self):
        self.fasta_file = get_templates_path().parent.joinpath('templates.fasta')
        self.format_str = 'fasta'

    def get_sequence_of_structure(self, structure: str) -> str:
        return [
            str(rec.seq) for rec in SeqIO.parse(self.fasta_file, self.format_str)
            if structure == rec.name
        ][0]

    def create_alignment_file(self, seq1: str, seq2: str, structure: str,
                              output_dir: Path) -> Path:
        if not output_dir.exists():
            logging.info(f"{output_dir} does not exists, creating...")
            os.mkdir(output_dir)

        alignment_file_name = 'alignment.pir'
        alignment_file_path = output_dir.joinpath(alignment_file_name)
        with open(alignment_file_path, 'w') as alignment_file_handle:
            template_seq = self.get_sequence_of_structure(structure)
            seq1, seq2, template_seq = self.align_sequences(seq1, seq2,
                                                       template_seq)

            print(">P1;template", file=alignment_file_handle)
            print("Structure:%s:FIRST:A:LAST:L::-1.00:-1.00:" % structure,
                  file=alignment_file_handle)

            for i in range(1, 4):
                print(textwrap.fill(template_seq, width=80) + '/',
                      file=alignment_file_handle)

            print(textwrap.fill(template_seq, width=80) + '*\n',
                  file=alignment_file_handle)

            print(">P1;sequence", file=alignment_file_handle)
            print("sequence:target::::::-1.00:-1.00:",
                  file=alignment_file_handle)
            for i in range(1, 3):
                print(textwrap.fill(seq1, width=80) + '/',
                      file=alignment_file_handle)

            print(textwrap.fill(seq2, width=80) + '/',
                  file=alignment_file_handle)
            print(textwrap.fill(seq2, width=80) + '*\n',
                  file=alignment_file_handle)
        return alignment_file_path

    def align_sequences(self, seq1: str, seq2: str,
                        t_seq: str) -> Tuple[str, str, str]:

        lseq1 = len(seq1)
        lseq2 = len(seq2)
        ltseq = len(t_seq)

        # Seq1 is the longest
        if lseq1 >= lseq2 and lseq1 >= ltseq:

            # Align template seq to seq1
            ldiff = len(seq1) - len(t_seq)
            tail = int(ldiff / 2) * '-'
            t_seq = tail + t_seq + tail

            # Align seq2 to seq1
            ldiff = len(seq1) - len(seq2)
            tail = int(ldiff / 2) * '-'
            seq2 = tail + seq2 + tail

        elif lseq2 >= lseq1 and lseq2 >= ltseq:
            # Align template seq to seq2
            ldiff = len(seq2) - len(t_seq)
            tail = int(ldiff / 2) * '-'
            t_seq = tail + t_seq + tail

            # Align seq1 to seq2
            ldiff = len(seq2) - len(seq1)
            tail = int(ldiff / 2) * '-'
            seq1 = tail + seq1 + tail

        else:
            # Align seq1 to template
            ldiff = len(t_seq) - len(seq1)
            tail = int(ldiff / 2) * '-'
            seq1 = tail + seq1 + tail

            # Align seq2 to template
            ldiff = len(t_seq) - len(seq2)
            tail = int(ldiff / 2) * '-'
            seq2 = tail + seq2 + tail

        return (seq1, seq2, t_seq)
