#!/bin/bash -e
export SERVICES_GJ_HOST=0.0.0.0
export SERVICES_GJ_PORT=8080
export SERVICES_GJ_ARTIFACT=$(mvn -q -Dexec.executable='echo' -Dexec.args='${project.groupId}.${project.artifactId}-${project.version}-jar-with-dependencies.${project.packaging}' --non-recursive org.codehaus.mojo:exec-maven-plugin:1.3.1:exec)
docker build --build-arg SERVICES_GJ_HOST=$SERVICES_GJ_HOST \
             --build-arg SERVICES_GJ_PORT=$SERVICES_GJ_PORT \
             --build-arg SERVICES_GJ_ARTIFACT=$SERVICES_GJ_ARTIFACT \
             -t tln-grizzly-jersey .
docker run -p $SERVICES_GJ_PORT:$SERVICES_GJ_PORT --rm tln-grizzly-jersey
docker rmi tln-grizzly-jersey
