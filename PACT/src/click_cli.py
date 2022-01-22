import click

from PACT.src.preprocessing import create_alignment_file
#from preprocessing import create_alignment_file

@click.command()
@click.option('--output', default='output', help="Path to alignment file to be created")
@click.option('--seq1', default='KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY', help="First sequence")
@click.option('--seq2', default='DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV', help="Second sequence")
@click.option('--structure', default='iapp', help="Structure ...")
@click.option('--fasta', default='../res/templates.fasta' , help="Fasta file...")
def create_alignment_file_CLI(output: str, seq1, seq2, structure, fasta):
    """Creates alignment file from two sequences of Amyloids"""
    create_alignment_file(output,seq1,seq2,structure,fasta)


if __name__ == '__main__':
    create_alignment_file_CLI()