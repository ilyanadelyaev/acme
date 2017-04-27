# acme

## neuro

Base: https://habrahabr.ru/company/dca/blog/274027/

Corpus: http://study.mokoron.com

### commands

prepare project

```make prepare```

```cp ./env/config/neuro/config.yml ./env/config/neuro/test.config.yml```
Настроить тестовый конфиг
```vim ./env/config/neuro/test.config.yml```

```make neuro_api__run```

prepare corpus

```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/prepare_corpus.py --positive-csv=./data/positive.csv --negative-csv=./data/negative.csv --corpus-out=./data/corpus.json```

train rnn

```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/train_rnn.py --corpus=./data/corpus.json --model-json-out=./data/model.json --model-h5-out=./data/model.h5```
