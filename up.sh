#!/bin/bash


export $(cat ./.env | grep -v ^# | xargs)

pushd services/api
export API_ARTIFACT=$(mvn -q -Dexec.executable='echo' -Dexec.args='${project.artifactId}-${project.version}-jar-with-dependencies.${project.packaging}' --non-recursive org.codehaus.mojo:exec-maven-plugin:1.3.1:exec)
popd

docker-compose up $1 --scale $LB_STATIC_WEB_NAME=$LB_STATIC_WEB_NUM --scale $LB_SERVICES_API_NAME=$LB_SERVICES_API_NUM
