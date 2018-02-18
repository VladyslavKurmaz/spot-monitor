#!/bin/bash -e

mvn archetype:generate \
    -DarchetypeArtifactId=jersey-quickstart-grizzly2 \
    -DarchetypeGroupId=org.glassfish.jersey.archetypes \
    -DinteractiveMode=false \
    -DgroupId=org.talan.services \
    -DartifactId=api \
    -Dpackage=org.talan.services.api \
    -Dversion=18.2.0-SNAPSHOT \
    -DarchetypeVersion=2.17