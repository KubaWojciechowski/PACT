import sys
import os
import pandas as pd

from PACT.input_parsing import input_parser
from PACT.input_validation import is_input_file_well_formed
from PACT.computation import compute_cross_model_interactions_concurently
from PACT.result_evaluation import compute_scores

if __name__ == '__main__':

    args = input_parser()

    input_file_path = args.input
    output_path = args.output

    if(is_input_file_well_formed(input_file_path)):
        print("Input correctly formatted, prociding...")
    else:
        sys.exit("Input not well formed, exiting...")

    # Modeling
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    else:
        sys.exit('Output directory already exist!')

    data = pd.read_csv(input_file_path)

    results = compute_cross_model_interactions_concurently(data)

    compute_scores(data, output_path, args.treshold)