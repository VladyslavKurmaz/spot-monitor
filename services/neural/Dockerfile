FROM ogvalt/basic:gpu-latest

RUN pip --no-cache-dir install mxnet-cu80==0.12.0b20171028 gunicorn requests gevent tensorflow-gpu==1.4.1

WORKDIR /scripts
COPY ./scripts /scripts/

CMD ["sh", "./configure.sh"]