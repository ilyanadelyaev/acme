__test_clean__:
	find ./acme/ -name ".cache" -exec rm -rf {} \; || true
	find ./acme/ -name "__pycache__" -exec rm -rf {} \; || true
	find ./acme/ -name "*.pyc" -exec rm -rf {} \;


prepare:
	virtualenv ./env/ve/
	#
	./env/ve/bin/pip install -U six
	./env/ve/bin/pip install -U packaging
	./env/ve/bin/pip install -U appdirs
	./env/ve/bin/pip install -U setuptools
	./env/ve/bin/pip install -r ./env/requirements.txt
	#
	mkdir -p env/logs/local/
	mkdir -p env/logs/test/


clean:
	rm -rf env/ve/
	rm -rf env/logs/
	#
	make __test_clean__


lib__test_lint:
	./env/ve/bin/pycodestyle --config='./env/config/pycodestyle' ./acme/lib/
	./env/ve/bin/pylint --rcfile="./env/config/pylintrc" --errors-only --reports=n ./acme/lib/
	#
	./env/ve/bin/pycodestyle --config='./env/config/pycodestyle' ./acme/tools/
	./env/ve/bin/pylint --rcfile="./env/config/pylintrc" --errors-only --reports=n ./acme/tools/

lib__test_unit:
	make __test_clean__
	#
	# PYTHONPATH="./:${PYTHONPATH}" ./env/ve/bin/py.test -vvv -c ./env/config/pytest.ini ./acme/lib/ -n4
	#
	PYTHONPATH="./:${PYTHONPATH}" ./env/ve/bin/py.test -vvv -c ./env/config/pytest.ini ./acme/tools/ -n4

lib__test:
	make lib__test_lint
	make lib__test_unit


neuro_core__test_lint:
	./env/ve/bin/pycodestyle --config='./env/config/pycodestyle' ./acme/neuro/logic/
	./env/ve/bin/pylint --rcfile="./env/config/pylintrc" --errors-only --reports=n ./acme/neuro/logic/
	#
	./env/ve/bin/pycodestyle --config='./env/config/pycodestyle' ./acme/neuro/scripts/
	./env/ve/bin/pylint --rcfile="./env/config/pylintrc" --errors-only --reports=n ./acme/neuro/scripts/

neuro_core__test_unit:
	make __test_clean__
	#
	# PYTHONPATH="./:${PYTHONPATH}" CONFIG="./env/config/neuro/test.config.yml" ./env/ve/bin/py.test -vvv -c ./env/config/pytest.ini ./acme/neuro/logic/ -n4
	#
	# PYTHONPATH="./:${PYTHONPATH}" CONFIG="./env/config/neuro/test.config.yml" ./env/ve/bin/py.test -vvv -c ./env/config/pytest.ini ./acme/neuro/scripts/ -n4

neuro_core__test:
	make neuro_core__test_lint
	make neuro_core__test_unit


neuro_api__test_lint:
	./env/ve/bin/pycodestyle --config='./env/config/pycodestyle' ./acme/neuro/api/
	./env/ve/bin/pylint --rcfile="./env/config/pylintrc" --errors-only --reports=n ./acme/neuro/api/

neuro_api__test_unit:
	make __test_clean__
	#
	PYTHONPATH="./:${PYTHONPATH}" CONFIG="./env/config/neuro/test.config.yml" ./env/ve/bin/py.test -vvv -c ./env/config/pytest.ini ./acme/neuro/api/ -n4

neuro_api__test:
	make neuro_api__test_lint
	make neuro_api__test_unit

neuro_api__build:
	rpmbuild -bb env/package/linux/neuro_api/rpm.spec


test_lint:
	make lib__test_lint
	make neuro_core__test_lint
	make neuro_api__test_lint

test:
	make lib__test
	make neuro_core__test
	make neuro_api__test

_build_:
	make neuro_api__build
