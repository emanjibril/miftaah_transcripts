build:
    docker buildx build --platform linux/amd64 -t emanjibril/miftaahtranscripts:latest .

push:
	docker push emanjibril/miftaahtranscripts
