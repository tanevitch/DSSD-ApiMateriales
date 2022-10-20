FROM python:3.10.7-alpine3.16

COPY ./ ./app
WORKDIR /app
RUN pip install -r requirements.txt 
CMD ["waitress-serve", "--port:8080", "--call", "app:create_app"]