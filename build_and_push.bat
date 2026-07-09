@echo off
REM Build and push Docker image to registry (Windows)

setlocal enabledelayedexpansion

set IMAGE_NAME=%1
if "!IMAGE_NAME!"=="" set IMAGE_NAME=amd-captivate-ai

set REGISTRY=%2
if "!REGISTRY!"=="" set REGISTRY=docker.io

set USERNAME=%3
if "!USERNAME!"=="" set USERNAME=your-docker-username

REM Build image
echo Building Docker image: !IMAGE_NAME!
docker build -t !IMAGE_NAME!:latest .

REM Tag for registry
set FULL_IMAGE_NAME=!REGISTRY!/!USERNAME!/!IMAGE_NAME!:latest
docker tag !IMAGE_NAME!:latest !FULL_IMAGE_NAME!

REM Push to registry
echo Pushing to !FULL_IMAGE_NAME!
docker push !FULL_IMAGE_NAME!

echo.
echo Image pushed successfully!
echo To use this image:
echo docker run -v C:\path\to\input:/input -v C:\path\to\output:/output !FULL_IMAGE_NAME!
