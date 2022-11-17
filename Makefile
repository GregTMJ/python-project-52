install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install --force-reinstall dist/*.whl

prepare-db:
	poetry run python manage.py migrate

serve:
	poetry run python manage.py runserver 0.0.0.0:8000

shell:
	poetry run python manage.py shell

check:
	poetry check

lint:
	poetry run flake8 .

update-locale:
	django-admin makemessages -l ru

compile-locales:
	django-admin compilemessages

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run --source='.' manage.py test task_manager
	coverage html
	coverage report
