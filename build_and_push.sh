#!/bin/bash
# Build and push Docker image to registry

# Configuration
IMAGE_NAME="${1:-amd-captivate-ai}"
REGISTRY="${2:-docker.io}"  # or your registry (e.g., ghcr.io, your-registry.azurecr.io)
USERNAME="${3:-your-docker-username}"

# Build image
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME:latest .

# Tag for registry
FULL_IMAGE_NAME="$REGISTRY/$USERNAME/$IMAGE_NAME:latest"
docker tag $IMAGE_NAME:latest $FULL_IMAGE_NAME

# Login to registry (if using Docker Hub, already logged in typically)
# docker login

# Push to registry
echo "Pushing to $FULL_IMAGE_NAME"
docker push $FULL_IMAGE_NAME

echo "✓ Image pushed successfully!"
echo "To use this image:"
echo "docker run -v /path/to/input:/input -v /path/to/output:/output $FULL_IMAGE_NAME"
