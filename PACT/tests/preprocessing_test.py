from PACT.src.preprocessing import align_sequences, get_template_sequence

def test_align_sequences():
    seq_1 = "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY"
    seq_2 = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV"
    t_seq = "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY"
    expected_seq1 = "-KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY-"
    expected_seq2 = "DAEFRHDSGYEVHHQKLVFFAEDVGSNKGAIIGLMVGGVV"
    expected_t_seq = "-KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY-"
    seq_1, seq_2, t_seq = align_sequences(seq_1, seq_2, t_seq)
    assert(seq_1 == expected_seq1)
    assert(seq_2 == expected_seq2)
    assert(t_seq == expected_t_seq)

def test_get_template_sequence():
    structure = 'iapp'
    template = '/PACT/PACT/res/templates.fasta'
    sequence = get_template_sequence(template, structure)
    assert(sequence == "KCNTATCATQRLANFLVHSSNNFGAILSSTNVGSNTY")
