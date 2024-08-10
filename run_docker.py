import os

IMAGE_NAME = 'rkd3d9/django:latest'
CONTAINER_NAME = 'augusta_crm'
LOCAL_PATH = str(input("Enter the local full path from source disk to the project DIR: "))

print(
    f"docker run -it --rm -p 9199:9199 -p 9099:9099 -p 9005:9005 -p 9000:9000 -p 8085:8085 -p 8080:8080 -p 5001:5001 -p 5000:5000 -p 4000:4000 -p 9299:9299 -p 9399:9399 -p 8000:8000 -v D:\rishi_sunak:/app --name {CONTAINER_NAME} {IMAGE_NAME}"
)
os.system(
    f'docker run -it --rm -p 9199:9199 -p 9099:9099 -p 9005:9005 -p 9000:9000 -p 8085:8085 -p 8080:8080 -p 5001:5001 -p 5000:5000 -p 4000:4000 -p 9299:9299 -p 9399:9399 -p 8000:8000 -v {LOCAL_PATH}:/app --name {CONTAINER_NAME} {IMAGE_NAME}'
)
