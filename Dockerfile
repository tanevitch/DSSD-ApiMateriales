FROM python:3.10.7-alpine3.16

COPY ./ ./app
WORKDIR /app
RUN pip install -r requirements.txt 
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]


