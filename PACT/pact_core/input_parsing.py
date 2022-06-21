import argparse
import click
import os
import sys
import pandas as pd

from input_validation import is_input_file_well_formed
from computation import compute_cross_model_interactions_concurently
from result_evaluation import compute_scores

@click.command
@click.option('--input', default='example.csv', help="Path to input file containing amyloid sequences")
@click.option('--output', default='output', help="Path to output folder for the results")
@click.option('--threshold', default=236, help="Energy threshold")
def PACT_main_CLI(input, output, threshold):

    if(is_input_file_well_formed(input)):
        print("Input correctly formatted, prociding...")
    else:
        sys.exit("Input not well formed, exiting...")

    # Modeling
    if not os.path.exists(output):
        os.mkdir(output)
    else:
        sys.exit('Output directory already exist!')

    data = pd.read_csv(input)

    results = compute_cross_model_interactions_concurently(data)

    compute_scores(data, output, threshold)
