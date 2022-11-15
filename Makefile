install:
	peotry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install --force-reinstall dist/*.whl


lint:
	poetry run flake8 task_manager