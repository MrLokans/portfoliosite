#!/bin/bash

# This script is used to build and push the back-end docker image
# to the private registry, where it may be picked up afterwards

set -e

DOCKERFILE_DIR=.
DOCKER_REGISTRY_URL=registry.mrlokans.com:5000

# Union of version, current date and git revision
IMAGE_VERSION="$(cat VERSION)-$(date +'%Y-%m-%d_%H-%M-%S')-$(git rev-parse --short --verify HEAD)"
IMAGE_NAME=personal_site
FULL_IMAGE_NAME=$DOCKER_REGISTRY_URL/$IMAGE_NAME:$IMAGE_VERSION
LATEST_IMAGE_NAME=$DOCKER_REGISTRY_URL/$IMAGE_NAME:latest

if [ -z "$DOCKER_USERNAME" ]; then
    echo "DOCKER_USERNAME environment variable is not set, failing."
    exit 1
fi

if [ -z "$DOCKER_PASSWORD" ]; then
    echo "DOCKER_PASSWORD environment variable is not set, failing."
    exit 1
fi

echo "Image version: $IMAGE_VERSION"

echo "Logging in into the docker registry."
echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin $DOCKER_REGISTRY_URL

echo "Pulling the latest image to make sure image cache is available."
docker pull $LATEST_IMAGE_NAME

echo "Build docker image."
docker build $DOCKERFILE_DIR -t "$FULL_IMAGE_NAME"

echo "Tagging the latest version."
docker tag $FULL_IMAGE_NAME $LATEST_IMAGE_NAME

echo "Pushing images to the registry."
docker push $FULL_IMAGE_NAME
docker push $LATEST_IMAGE_NAME