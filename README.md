# Augusta-CRM
# reconnect container
docker exec -it 79417d407676f242827d7bc95c7395e8a5ccb6ab9604ff76c417f915510d0ad1 bash

# run image container
docker run -it --gpus -all -p 8000:8000 -v D:\rishi_sunak:/app rkd3d9/django:latest bash 