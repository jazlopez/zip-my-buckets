env:
	virtualenv --clear \
	--no-setuptools \
	--no-wheel \
	--verbose \
	--no-download \
	--always-copy \
	--python=python3 . && sleep 1 && source bin/activate

clean:
	rm -rf bin/ \
	lib/ \
	include/ \
	.Python \
	pip-selfcheck.json

test:
	python tests.py

coverage:
	coverage3 run tests.py && coverage3 html -d output_html/