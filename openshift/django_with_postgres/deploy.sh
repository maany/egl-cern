#!/usr/bin/env bash

docker build --tag openshift-egl-django .
docker tag openshift-egl-django maany/openshift-egl-django
docker login
docker push maany/openshift-egl-django

oc delete all -l app=egl-cern
oc new-app maany/openshift-egl-django~https://github.com/maany/egl-cern --env-file ../../.env.okd
