    ┏━┓┏━┓╺┳┓╻┏━┓┏━╸╻┏━╸╻  ┏━╸╺┳╸╺┳╸┏━┓
    ┣┳┛┣━┫ ┃┃┃┃ ┃┃  ┃┃  ┃  ┣╸  ┃  ┃ ┣━┫
    ╹┗╸╹ ╹╺┻┛╹┗━┛┗━╸╹┗━╸┗━╸┗━╸ ╹  ╹ ╹ ╹
    =======================================================================

sono 2 (per adesso) applicazioni per GAE (appengine.google.com).
 * cdn é semplicemente un servitore di risorse statiche (magari piú avanti tuniamo le varie risorse/cache)
 * radiocicletta-server é l'applicazione vera


Richiede python2.7 e virtualenv e Appengine SDK
Basato su django-nonrel https://github.com/django-nonrel/django-nonrel

Per inizializzare l'ambiente di sviluppo:

    $ git clone https://github.com/radiocicletta/radiociblog
    $ virtualenv radiociblog
    $ cd radiociblog
    $ source bin/activate

Per scaricare la prima volta i pacchetti necessari

    (virtualenv)$ ./buildenv.sh create

Per ricreare l'ambiente di svilppo in un repository esistente

    (virtualenv)$ ./buildenv.sh replace

_buildenv.sh_ effettua il download e il patching delle librerie necessarie.

Per installare Appengine SDK su OSX: scaricare il pacchetto autoinstallante da https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
Per installare Appengine SDK su Linux da virtualenv:

    pip install -e git+https://github.com/davidwtbuxton/appengine.py.git#egg=appengine
    appengine.py [url dello zip in  https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python]

Deploy
======

Radiocicletta-server
--------------------

dalla directory root del repo:

    $ python radiocicletta-server/manage.py deploy

Cdn
---

dalla directory root del repo:

    $ dev_app update cdn/
