# acme

## neuro

Base: https://habrahabr.ru/company/dca/blog/274027/

Corpus: http://study.mokoron.com

### commands

```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/process_corpus.py --corpus-csv=./data/positive.csv```

```PYTHONPATH=./ CONFIG=./env/config/neuro/test.config.yml python acme/neuro/scripts/fetch_tweets.py --lang=ru --search="яндекс"```
