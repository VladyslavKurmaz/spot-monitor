FROM ogvalt/basic:cpu-latest

RUN pip install gunicorn requests flask_cors

COPY ./service/ /workspace/

WORKDIR /workspace

CMD ["gunicorn", "-c", "./gunicorn.conf", "wsgi:app"]