#!/usr/bin/env bash

# Build the docker image
docker build -t onshape-git-sync .

# Run docker
docker run --rm \
 --env-file docker.env \
 -v "$(pwd)/logs:/app/logs" \
 -v "$(pwd)/snapshots:/app/snapshots" \
 onshape-git-sync
