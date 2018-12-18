FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ls
RUN pwd
RUN python manage.py collectstatic --noinput
EXPOSE 8000

