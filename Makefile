


deploy:
	git pull
	docker rm -f edbm || echo "no container named edbm"
	docker build -t edbm .
	docker run --name edbm -d -v /root/edbm34_ugc/edbm34_ugc:/edbm34_ugc -p 8085:8000 edbm
