FROM python:3.10.7-alpine3.16

COPY ./ ./app
WORKDIR /app
RUN pip install -r requirements.txt 
CMD ["gunicorn", "run:create_app()"]