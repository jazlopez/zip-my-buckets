test:
	python tests.py

coverage:
	coverage3 run tests.py && coverage3 html -d output_html/


