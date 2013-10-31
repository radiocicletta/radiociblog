#!/bin/sh


function do_create {

[ ! -d build ] && mkdir build

pip install --download='./build' --no-install -r requirements.txt

unzip -q build/django-autoload-*.zip -d build
unzip -q build/django-dbindexer-*.zip -d build
unzip -q build/django-1.4.9.zip -d build
unzip -q build/djangoappengine-*.zip -d build
unzip -q build/djangotoolbox-*.zip -d build
unzip -q build/django-permission-backend-nonrel*.zip -d build
unzip -q build/gaepytz-*.zip -d build
tar -jxvf build/pytz-*.tar.bz2 -C build
tar -zxvf build/django-admin-bootstrapped-*.tar.gz -C build

cp -r build/django-autoload/autoload ./radiocicletta-server/autoload
cp -r build/django-dbindexer/dbindexer ./radiocicletta-server/dbindexer
cp -r build/django/django ./radiocicletta-server/django
cp -r build/djangoappengine/djangoappengine ./radiocicletta-server/djangoappengine
cp -r build/djangotoolbox/djangotoolbox ./radiocicletta-server/djangotoolbox
cp -r build/django-permission-backend-nonrel/permission_backend_nonrel ./radiocicletta-server/permission_backend_nonrel
cp -R build/pytz-*/pytz/ ./radiocicletta-server/pytz
cp -R build/gaepytz/pytz/ ./radiocicletta-server/pytz
rm -rf ./radiocicletta-server/pytz/zoneinfo
cp -r build/django-admin-bootstrapped-0.4.3/django_admin_bootstrapped ./radiocicletta-server/django_admin_bootstrapped

}

function do_removepackages {

rm -rf ./radiocicletta-server/autoload
rm -rf ./radiocicletta-server/dbindexer
rm -rf ./radiocicletta-server/django
rm -rf ./radiocicletta-server/djangoappengine
rm -rf ./radiocicletta-server/djangotoolbox
rm -rf ./radiocicletta-server/permission_backend_nonrel
rm -rf ./radiocicletta-server/pytz
rm -rf ./radiocicletta-server/django_admin_bootstrapped

}

function do_clean {

rm -rf ./build ./src

}

case "$1" in
    create)
        echo "Creating environment"
        do_create
        ;;
    replace)
        echo "Recreating environment"
        do_removepackages
        do_create
        ;;
    clean)
        echo "Cleaning environment"
        do_clean
        ;;
    *)
        echo "Usage: $0 {create|replace|clean}"
        exit 1
        ;;
esac

exit 0
