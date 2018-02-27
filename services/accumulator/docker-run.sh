#!/bin/bash -e
export SERVICES_ACCUMULATOR_HOST=0.0.0.0
export SERVICES_ACCUMULATOR_PORT=8081
export SERVICES_ACCUMULATOR_ARTIFACT=$(mvn -q -Dexec.executable='echo' -Dexec.args='${project.groupId}.${project.artifactId}-${project.version}-jar-with-dependencies.${project.packaging}' --non-recursive org.codehaus.mojo:exec-maven-plugin:1.3.1:exec)
echo $SERVICES_ACCUMULATOR_ARTIFACT
docker build --build-arg SERVICES_ACCUMULATOR_HOST=$SERVICES_ACCUMULATOR_HOST \
             --build-arg SERVICES_ACCUMULATOR_PORT=$SERVICES_ACCUMULATOR_PORT \
             --build-arg SERVICES_ACCUMULATOR_ARTIFACT=$SERVICES_ACCUMULATOR_ARTIFACT \
             -t tln-grizzly-jersey:latest .
docker run --rm -d -p $SERVICES_ACCUMULATOR_PORT:$SERVICES_ACCUMULATOR_PORT --name tln-grizzly-jersey tln-grizzly-jersey:latest
