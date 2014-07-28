    ┏━┓┏━┓╺┳┓╻┏━┓┏━╸╻┏━╸╻  ┏━╸╺┳╸╺┳╸┏━┓
    ┣┳┛┣━┫ ┃┃┃┃ ┃┃  ┃┃  ┃  ┣╸  ┃  ┃ ┣━┫
    ╹┗╸╹ ╹╺┻┛╹┗━┛┗━╸╹┗━╸┗━╸┗━╸ ╹  ╹ ╹ ╹
    =======================================================================

 * cdn è un servitore di risorse statiche su GAE (appengine.google.com)
 * radiocicletta-server è l'applicazione basata su django 1.6.5

Richiede python2.7 e virtualenv e Appengine SDK

Per inizializzare l'ambiente di sviluppo:

    $ git clone https://github.com/radiocicletta/radiociblog
    $ virtualenv radiociblog/venv
    $ cd radiociblog
    $ source venv/bin/activate

Deploy
======

Radiocicletta-server
--------------------

dalla directory root del repo:

    (virtualenv)$ python radiocicletta-server/manage.py deploy

Cdn
---

dalla directory root del repo:

    (virtualenv)$ dev_app update cdn/
