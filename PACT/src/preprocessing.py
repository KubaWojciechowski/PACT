from Bio import SeqIO
import textwrap

# should probably be called get template sequence
def get_template_sequence(fasta, template):
    record = SeqIO.parse(fasta, 'fasta')

    for i in record:
        if template == i.name:
            return str(i.seq)


def align_sequences(seq1, seq2, t_seq):

    lseq1 = len(seq1)
    lseq2 = len(seq2)
    ltseq = len(t_seq)

    # Seq1 is the longest
    if lseq1 >= lseq2 and lseq1 >= ltseq:

        # Align template seq to seq1
        ldiff = len(seq1)-len(t_seq)
        tail = int(ldiff/2) * '-'
        t_seq = tail + t_seq + tail

        # Align seq2 to seq1
        ldiff = len(seq1)-len(seq2)
        tail = int(ldiff/2) * '-'
        seq2 = tail + seq2 + tail

    elif lseq2 >= lseq1 and lseq2 >= ltseq:
        # Align template seq to seq2
        ldiff = len(seq2)-len(t_seq)
        tail = int(ldiff/2) * '-'
        t_seq = tail + t_seq + tail

        # Align seq1 to seq2
        ldiff = len(seq2)-len(seq1)
        tail = int(ldiff/2) * '-'
        seq1 = tail + seq1 + tail

    else:
        # Align seq1 to template
        ldiff = len(t_seq)-len(seq1)
        tail = int(ldiff/2) * '-'
        seq1 = tail + seq1 + tail

        # Align seq2 to template
        ldiff = len(t_seq)-len(seq2)
        tail = int(ldiff/2) * '-'
        seq2 = tail + seq2 + tail

    return(seq1, seq2, t_seq)

# unfortunately alignment file is needed by the modeller, so we need to make this files system write
def create_alignment_file(pathToAlignmentFile : str, seq1, seq2, structure, fasta):
    template_seq = get_template_sequence(fasta, structure)
    alignmentFileName = 'alignment.pir'
    alignmentFile = open(pathToAlignmentFile+alignmentFileName, 'w') 
    seq1, seq2, template_seq = align_sequences(seq1, seq2, template_seq)

    print(">P1;template", file=alignmentFile)
    print("Structure:%s:FIRST:A:LAST:L::-1.00:-1.00:" %
          structure, file=alignmentFile)

    for i in range(1, 4):
        print(textwrap.fill(template_seq, width=80) + '/', file=alignmentFile)

    print(textwrap.fill(template_seq, width=80) + '*\n', file=alignmentFile)

    print(">P1;sequence", file=alignmentFile)
    print("sequence:target::::::-1.00:-1.00:", file=alignmentFile)
    for i in range(1, 3):
        print(textwrap.fill(seq1, width=80) + '/', file=alignmentFile)

    print(textwrap.fill(seq2, width=80) + '/', file=alignmentFile)
    print(textwrap.fill(seq2, width=80) + '*\n', file=alignmentFile)

    alignmentFile.close()

    return alignmentFileName