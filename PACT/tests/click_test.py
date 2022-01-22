import os
from click.testing import CliRunner
from PACT.src.click_cli import create_alignment_file_CLI

# TO-DO: Work on filesystem isolation
# possibly could be integrated with pytest to remove tmp files
def test_create_alignment_file():
    runner = CliRunner()
    #with runner.isolated_filesystem():
    result = runner.invoke(create_alignment_file_CLI,['--output','outputFolder',
    '--seq1','KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY',
    '--seq2','DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV',
    '--structure','iapp',
    '--fasta', 'PACT/res/templates.fasta'])
    assert result.exit_code == 0
    assert os.path.exists('outputFolder') == True