#!/usr/bin/env bash

docker build --tag openshift-egl-django .
docker tag openshift-egl-django borisvasilev/openshift-egl-django
docker login
docker push borisvasilev/openshift-egl-django

oc delete all -l app=egl-cern
oc new-app borisvasilev/openshift-egl-django~https://github.com/boris-vasilev/egl-cern --env-file ../../.env.okd
oc expose svc/egl-cern
oc annotate route egl-cern --overwrite haproxy.router.openshift.io/timeout=15m
oc annotate route egl-cern router.cern.ch/network-visibility=Internet