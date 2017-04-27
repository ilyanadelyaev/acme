import json
import argparse

import acme.neuro.scripts.helpers as _helpers
_helpers.setup_logging()

import acme.neuro.logic.corpus as _corpus


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--positive-csv')
    parser.add_argument('--negative-csv')
    parser.add_argument('--corpus-out')
    args = parser.parse_args()

    dictionary = {}
    data = []

    dictionary, data = _corpus.process_csv(
        file_path=args.positive_csv,
        dictionary=dictionary,
        data=data,
    )
    dictionary, data = _corpus.process_csv(
        file_path=args.negative_csv,
        dictionary=dictionary,
        data=data,
    )

    print 'dictionary size =', len(dictionary)
    print 'data size =', len(data)

    with open(args.corpus_out, 'wb') as f:
        f.write(json.dumps({
            'dictionary': dictionary,
            'data': data,
        }))
