# acme

## neuro

Base: https://habrahabr.ru/company/dca/blog/274027/

Corpus: http://study.mokoron.com

### commands

prepare corpus
```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/prepare_corpus.py --positive-csv=./data/positive.csv --negative-csv=./data/negative.csv --corpus-out=./data/corpus.json```

test twitter fetch
```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/fetch_tweets.py --lang=ru --search="яндекс"```

test train rnn
```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/train_rnn.py --corpus=./data/corpus.json```
