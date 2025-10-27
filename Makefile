# run from the root dir not the inside of the 05- folder
build-course-docker:
	podman build -t course-predictor -f notebooks/05-deployment/Dockerfile .

# run from root dir
run-course-docker:
	podman run -it --rm -p 9696:9696 course-predictor


# debug their docker
debug:
	podman run -it --rm agrigorev/zoomcamp-model:2025 /bin/bash

# build their docker
build-their-docker:
	podman build --platform linux/amd64 -t homework-05 -f notebooks/05-deployment/Dockerfile2 .

# run their docker
run-their-docker: build-their-docker
	podman run --platform linux/amd64 -it --rm -p 9696:9696 homework-05
