import json
import argparse

import acme.neuro.scripts.helpers as _helpers
_helpers.setup_logging()

import acme.neuro.logic.rnn as _rnn


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus')
    args = parser.parse_args()

    with open(args.corpus, 'rb') as f:
        raw_data = json.loads(f.read())

    dictionary = raw_data['dictionary']
    positive_data = raw_data['positive_data']
    negative_data = raw_data['negative_data']

    print 'dictionary size =', len(dictionary)
    print 'positive_data size =', len(positive_data)
    print 'negative_data size =', len(negative_data)

    _rnn.train_model(
        dictionary_size=len(dictionary),
        positive_data=positive_data,
        negative_data=negative_data,
    )
