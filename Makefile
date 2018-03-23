test:
	watchmedo shell-command --command="run-contexts -v" -R -W .
setup:
	pip install -r requirements.txt
	pip install -e .
mongo:
		docker run  -p 27017:27017 -d mongo
serve:
	cd slides
	python -m http.server
