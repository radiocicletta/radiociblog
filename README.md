    ┏━┓┏━┓╺┳┓╻┏━┓┏━╸╻┏━╸╻  ┏━╸╺┳╸╺┳╸┏━┓
    ┣┳┛┣━┫ ┃┃┃┃ ┃┃  ┃┃  ┃  ┣╸  ┃  ┃ ┣━┫
    ╹┗╸╹ ╹╺┻┛╹┗━┛┗━╸╹┗━╸┗━╸┗━╸ ╹  ╹ ╹ ╹
    =======================================================================

sono 2 (per adesso) applicazioni per GAE (appengine.google.com).
 * cdn é semplicemente un servitore di risorse statiche (magari piú avanti tuniamo le varie risorse/cache)
 * radiocicletta-server é l'applicazione vera


Richiede python2.7 e virtualenv e Appengine SDK
Basato su django-nonrel https://github.com/django-nonrel/django-nonrel

Per ricreare l'ambiente di sviluppo:

    $ git clone https://github.com/radiocicletta/radiociblog
    $ virtualenv radiociblog
    $ cd radiociblog
    $ source bin/activate
    $ ./buildenv.sh

_buildenv.sh_ effettua il download e il patching delle librerie necessarie.

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
