import argparse

import acme.neuro.scripts.helpers as _helpers
_helpers.setup_logging()

import acme.neuro.logic.corpus as _corpus


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus-csv')
    args = parser.parse_args()

    data, dictionary = _corpus.process_csv(
        file_path=args.corpus_csv,
    )
