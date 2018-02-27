#!/bin/bash


export $(cat ./.env | grep -v ^# | xargs)

pushd services/api
export SERVICES_API_ARTIFACT=$(mvn -q -Dexec.executable='echo' -Dexec.args='${project.groupId}.${project.artifactId}-${project.version}-jar-with-dependencies.${project.packaging}' --non-recursive org.codehaus.mojo:exec-maven-plugin:1.3.1:exec)
popd

pushd services/accumulator
export SERVICES_ACCUMULATOR_ARTIFACT=$(mvn -q -Dexec.executable='echo' -Dexec.args='${project.groupId}.${project.artifactId}-${project.version}-jar-with-dependencies.${project.packaging}' --non-recursive org.codehaus.mojo:exec-maven-plugin:1.3.1:exec)
popd


docker-compose up $1 --scale $LB_STATIC_DASHBOARD_NAME=$LB_STATIC_DASHBOARD_NUM --scale $LB_SERVICES_API_NAME=$LB_SERVICES_API_NUM
