FROM ogvalt/basic:gpu-latest

RUN pip --no-cache-dir install mxnet-cu80==0.12.0b20171028 gunicorn

WORKDIR /scripts
COPY ./scripts /scripts/

CMD ./configure.sh
