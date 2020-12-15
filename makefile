pull:
	git pull origin master
	
push:	
	git add -f .
	git commit -m "$(m)"
	git push origin master

