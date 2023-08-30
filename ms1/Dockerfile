FROM python:3.11.4-alpine3.17

WORKDIR /app
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

RUN adduser -S www-data -G www-data

RUN chown -R www-data:www-data /app/*

USER www-data

CMD ["python", "manage.py", "runserver", "0.0.0.0:7000"]