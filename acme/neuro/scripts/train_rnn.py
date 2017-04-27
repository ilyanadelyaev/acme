import json
import argparse

import acme.neuro.scripts.helpers as _helpers
_helpers.setup_logging()

import acme.neuro.logic.rnn as _rnn


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus')
    parser.add_argument('--model-json-out')
    parser.add_argument('--model-h5-out')
    args = parser.parse_args()

    with open(args.corpus, 'rb') as f:
        raw_data = json.loads(f.read())

    dictionary = raw_data['dictionary']
    data = raw_data['data']

    model = _rnn.train_model(
        dictionary=dictionary,
        data=data,
    )

    with open(args.model_json_out, 'wb') as f:
        f.write(model.to_json())
    model.save_weights(args.model_h5_out)

    _rnn.check_model(
        model=model,
        dictionary=dictionary,
        data=data,
    )
