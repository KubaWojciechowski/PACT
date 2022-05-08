from PACT.src.input_validation import is_input_file_well_formed
from PACT.src.computation import compute_cross_model_interactions_concurently
from PACT.src.result_evaluation import create_meta_file, find_minimum_energies, save_results_to_file
import click
from pathlib import Path
import pandas as pd

@click.command()
@click.option('--input_file', default='example.csv', help='input file')
@click.option('--output_dir', default='output', help='output directory')
@click.option('--threshold', default=236, help="Energy threshold")
def main_cli(input_file, output_dir, threshold):
    input_file = Path(input_file)
    if not is_input_file_well_formed(input_file):
        raise Exception(f"Input file {input_file} is not well formed")

    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    else:
        raise Exception(f"Output directory {output_dir} already exists")

    data = pd.read_csv(str(input_file))

    seq_list1 = data['seq1']
    seq_list2 = data['seq2']

    meta_file_path = create_meta_file(seq_list1, seq_list2, output_dir)
    compute_cross_model_interactions_concurently(data, output_dir)
    meta_file = pd.read_csv(meta_file_path)
    energy_file_path = output_dir.joinpath('energy.csv')
    energies = pd.read_csv(energy_file_path)
    min_energies = find_minimum_energies(energies, meta_file, threshold)
    save_results_to_file(min_energies, data, output_dir)

if __name__ == "__main__":
    main_cli()