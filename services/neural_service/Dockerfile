FROM ogvalt/basic:gpu-latest

RUN pip --no-cache-dir install mxnet-cu80==0.12.0b20171028 gunicorn

COPY ./service /workspace/

RUN chmod 777 /workspace/start.sh
RUN chmod 777 /workspace/configure.sh
RUN chmod 777 /workspace/app/deformable_detector/libs/init.sh

WORKDIR workspace

CMD ./configure.sh