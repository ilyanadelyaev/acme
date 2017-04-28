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



Setup HEROKU

```curl --upload-file ./data/model.h5 https://transfer.sh/model.h5```

```heroku run --app acme-neuro-app bash```

```
mkdir vim
curl https://s3.amazonaws.com/heroku-vim/vim-7.3.tar.gz --location --silent | tar xz -C vim
export PATH=$PATH:/app/vim/bin
```

```wget "https://transfer.sh/xcGGj/model.h5"```
```mv model.h5 data/```

```vim ./config.yml```

```heroku restart --app acme-neuro-app```
