FROM python:3.12
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /webapp
COPY Requirments.txt /webapp/Requirments.txt
RUN pip install -r Requirments.txt
COPY . /webapp

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
# CMD [ "python", "manage.py", "makemigrations";"python", "manage.py", "migrate"; "python", "manage.py", "runserver", "0.0.0.0:8000" ]

