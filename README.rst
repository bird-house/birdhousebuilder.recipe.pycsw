*****************************
birdhousebuilder.recipe.pycsw
*****************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.pycsw`` is a `Buildout`_ recipe to install and configure `pycsw`_ with `Anaconda`_. `pycsw`_ is a Python implementation of a `Catalog Service for the Web`_ (CSW). ``pycsw`` will be deployed as a `Supervisor`_ service and is available on a `Nginx`_ web server. 

Birdhousebuilder recipes are used to build Web Processing Service components (Phoenix, Malleefowl, Nighthawk, FlyingPigeon, ...) of the ClimDaPs project. All Birdhousebuilder recipes need an existing `Anaconda`_ installation.  

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`Supervisor`: http://supervisord.org/
.. _`Nginx`: http://nginx.org/
.. _`pycsw`: http://pycsw.org/
.. _`Catalog Service for the Web`: https://en.wikipedia.org/wiki/Catalog_Service_for_the_Web


Usage
*****

The recipe requires that Anaconda is already installed. It assumes that Anaconda is installed at the default location in your home directory ``~/anaconda``. Otherwise you need to set the Buildout option ``anaconda-home`` to the correct location.

It installs the ``pycsw`` package from a conda channel and setups a `pycsw`_ database (``sqlite``) in ``~/anaconda/var/lib/pycsw``. It deploys a `Supervisor`_ configuration for ``pycsw`` in ``~/anaconda/etc/supervisor/conf.d/pycsw.conf``. Supervisor can be started with ``~/anaconda/etc/init.d/supervisor start``.

The recipe will install the ``nginx`` package from a conda channel and deploy a Nginx site configuration for ``pycsw``. The configuration will be deployed in ``~/anaconda/etc/nginx/conf.d/pycsw.conf``. Nginx can be started with ``~/anaconda/etc/init.d/nginx start``.

By default ``pycsw`` will be available on http://localhost:8082/csw?service=CSW&version=2.0.2&request=GetCapabilities.

The recipe depends on ``birdhousebuilder.recipe.conda``, ``birdhousebuilder.recipe.supervisor`` and ``birdhousebuilder.recipe.nginx``.

Supported options
=================

The recipe supports the following options:

``anaconda-home``
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

``hostname``
   The hostname of the pycsw service (nginx). Default: ``localhost``

``port``
   The port of the pycsw service (nginx). Default: ``8082``   


Example usage
=============

The following example ``buildout.cfg`` installs ``pycsw`` with Anaconda::

  [buildout]
  parts = pycsw

  anaconda-home = /home/myself/anaconda

  [pycsw]
  recipe = birdhousebuilder.recipe.pycsw
  hostname = localhost
  port = 8082

After installing with Buildout start the ``pycsw`` service with::

  $ cd /home/myself/anaconda
  $ etc/init.d/supervisord start  # start|stop|restart
  $ etc/init.d/nginx start        # start|stop|restart
  $ bin/supervisorctl status      # check that pycsw is running
  $ less var/log/pycsw/pycsw.log  # check log file

Open your browser with the following URL:: 

  http://localhost:8082/csw?service=CSW&version=2.0.2&request=GetCapabilities





