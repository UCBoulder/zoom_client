install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

format:
	black zoom_client tests

lint:
	pylint zoom_client tests --extension-pkg-whitelist=pyarrow &&\
	black zoom_client tests --check &&\
	bandit -r zoom_client -x ./tests -s B104

test:
	pytest -o log_cli=true
