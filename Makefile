test:
	- run-contexts -v
	watchmedo shell-command --command="run-contexts -v" -R -W .
mongo:
		docker run  -p 27017:27017 -d mongo
serve:
	cd slides
	python -m http.server
