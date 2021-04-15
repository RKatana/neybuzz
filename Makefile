serve:
	python3 manage.py runserver

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

shell:
	python manage.py shell

admin:
	python manage.py createsuperuser
	
test:
	coverage run manage.py test && coverage html