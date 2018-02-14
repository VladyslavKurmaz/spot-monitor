FROM openjdk:8u151-jre-alpine

ARG SERVICES_API_ARTIFACT
ARG SERVICES_API_HOSTNAME
ARG SERVICES_API_PORT

ENV SERVICES_API_ARTIFACT $SERVICES_API_ARTIFACT
ENV SERVICES_API_HOSTNAME $SERVICES_API_HOSTNAME
ENV SERVICES_API_PORT $SERVICES_API_PORT

RUN apk --update --no-cache add curl python py-pip && pip install jsonschema requests

COPY ./target/${SERVICES_API_ARTIFACT} /
RUN mkdir scripts
COPY ./scripts /scripts
#HEALTHCHECK --interval=5s --timeout=3s CMD curl --fail http://localhost:${API_PORT}/healthcheck || exit 1

CMD exec java -jar /${SERVICES_API_ARTIFACT}
