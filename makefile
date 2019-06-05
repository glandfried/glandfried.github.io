pull:
	git pull
	
push:	
	git add -f .
	git commit -m "$(m)"
	git push origin master

