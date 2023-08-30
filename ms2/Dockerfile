FROM python:3.11.4-alpine3.17

WORKDIR /sanic

COPY . .

RUN pip install -r requirements.txt

RUN adduser -S www-data -G www-data

RUN chown -R www-data:www-data /sanic/*

USER www-data

EXPOSE 8000

CMD ["python", "server.py"]
