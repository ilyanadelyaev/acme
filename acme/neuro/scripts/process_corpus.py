import argparse

import acme.neuro.scripts.helpers as _helpers
_helpers.setup_logging()

import acme.neuro.logic.corpus as _corpus


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus-file')
    args = parser.parse_args()

    raw_data = _corpus.prepare(
        file_path=args.corpus_file,
    )

    data, dictionary = _corpus.encode_to_numbers(
        raw_data=raw_data,
    )

    print data[-1]
