clean:
	find -name "*.pyc" -type f -delete
	find -name "__pycache__" -type d -delete

prepare:
	python3 manage.py migrate
	python3 "scripts/mfl.py"
	python3 "scripts/populate.py"
	python3 "scripts/create_users.py"
