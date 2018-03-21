FROM ogvalt/basic:cpu-latest

RUN pip install gunicorn requests

WORKDIR /scripts
COPY ./scripts/ /scripts/

CMD ./start.sh