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

    positive_data, dictionary = _corpus.process_csv(
        file_path=args.positive_csv,
        dictionary=dictionary,
    )
    negative_data, dictionary = _corpus.process_csv(
        file_path=args.negative_csv,
        dictionary=dictionary,
    )

    print 'dictionary size =', len(dictionary)
    print 'positive_data size =', len(positive_data)
    print 'negative_data size =', len(negative_data)

    with open(args.corpus_out, 'wb') as f:
        f.write(json.dumps({
            'dictionary': dictionary,
            'positive_data': positive_data,
            'negative_data': negative_data,
        }))
