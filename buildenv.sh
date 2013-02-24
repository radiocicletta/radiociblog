#!/bin/sh

mkdir build

pip install --download='./build' --no-install -r requirements.txt

unzip -q build/django-autoload-*.zip -d build
unzip -q build/django-dbindexer-*.zip -d build
unzip -q build/django-nonrel-*.zip -d build
unzip -q build/djangoappengine-*.zip -d build
unzip -q build/djangotoolbox-*.zip -d build
unzip -q build/gaepytz-*.zip -d build
tar -zxvf build/pytz-*.tar.gz -C build

cp -r build/django-autoload/autoload ./radiocicletta-server/autoload
cp -r build/django-dbindexer/dbindexer ./radiocicletta-server/dbindexer
cp -r build/django-nonrel/django ./radiocicletta-server/django
cp -r build/djangoappengine/djangoappengine ./radiocicletta-server/djangoappengine
cp -r build/djangotoolbox/djangotoolbox ./radiocicletta-server/djangotoolbox
cp -r build/pytz-*/pytz ./radiocicletta-server/pytz
cp -R build/gaepytz/pytz/ ./radiocicletta-server/pytz
rm -rf ./radiocicletta-server/pytz/zoneinfo


rm -rf ./radiocicletta-server/djangoappengine/djangoappengine.egg-info
rm -rf ./build ./src
