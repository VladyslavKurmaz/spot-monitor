FROM ogvalt/basic:cpu-latest

RUN pip install gunicorn requests gevent

WORKDIR /scripts
COPY ./scripts/ /scripts/

CMD ["gunicorn", "-c", "./gunicorn.conf", "wsgi:app"]
