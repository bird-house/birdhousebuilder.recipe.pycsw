*****************************
birdhousebuilder.recipe.pycsw
*****************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.pycsw`` is a `Buildout`_ recipe to install and configure `pycsw`_ with `Anaconda`_. `pycsw`_ is a Python implementation of a `Catalog Service for the Web`_ (CSW). ``pycsw`` will be deployed as a `Supervisor`_ service and is available on a `Nginx`_ web server. 

This recipe is used by the `Birdhouse`_ project. 

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`Supervisor`: http://supervisord.org/
.. _`Nginx`: http://nginx.org/
.. _`pycsw`: http://pycsw.org/
.. _`Catalog Service for the Web`: https://en.wikipedia.org/wiki/Catalog_Service_for_the_Web
.. _`Birdhouse`: http://bird-house.github.io/


Usage
*****

The recipe requires that Anaconda is already installed. It assumes that the default Anaconda location is in your home directory ``~/anaconda``. Otherwise you need to set the ``ANACONDA_HOME`` environment variable or the Buildout option ``anaconda-home``.

It installs the ``pycsw`` package from a conda channel in a conda environment named ``birdhouse``. The location of the birdhouse environment is ``.conda/envs/birdhouse``. It setups a `pycsw`_ database (``sqlite``) in ``~/.conda/envs/birdhouse/var/lib/pycsw``. It deploys a `Supervisor`_ configuration for ``pycsw`` in ``~/.conda/envs/birdhouse/etc/supervisor/conf.d/pycsw.conf``. Supervisor can be started with ``~/.conda/envs/birdhouse/etc/init.d/supervisor start``.

The recipe will install the ``nginx`` package from a conda channel and deploy a Nginx site configuration for ``pycsw``. The configuration will be deployed in ``~/.conda/envs/birdhouse/etc/nginx/conf.d/pycsw.conf``.

By default ``pycsw`` will be available on http://localhost:8082/csw?service=CSW&version=2.0.2&request=GetCapabilities.

The recipe depends on ``birdhousebuilder.recipe.conda``, ``birdhousebuilder.recipe.supervisor`` and ``birdhousebuilder.recipe.nginx``.

Supported options
=================

The recipe supports the following options:

**anaconda-home**
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.
   The default location can also be set with the environment variable ``ANACONDA_HOME``. Example:

.. code-block:: sh

     export ANACONDA_HOME=/opt/anaconda

 Search priority is:

 1. ``anaconda-home`` in ``buildout.cfg``
 2. ``$ANACONDA_HOME``
 3. ``$HOME/anaconda``

**hostname**
   The hostname of the pycsw service (nginx). Default: ``localhost``

**port**
   The port of the pycsw service (nginx). Default: ``8082``   

**transactions**
   Allow transactions. Default: ``true``

**allowed_ips**
   The IP addresses allowed to perform transactions. Default: ``127.0.0.1``


See the `PyCSW documentation <http://docs.pycsw.org/en/latest/configuration.html>`_ for configuration details.

Example usage
=============

The following example ``buildout.cfg`` installs ``pycsw`` with Anaconda:

.. code-block:: ini

  [buildout]
  parts = pycsw

  anaconda-home = /opt/anaconda

  [pycsw]
  recipe = birdhousebuilder.recipe.pycsw
  hostname = localhost
  port = 8082

After installing with Buildout start the ``pycsw`` service with:

.. code-block:: sh

  $ cd /home/myself/.conda/envs/birdhouse
  $ etc/init.d/supervisord start       # start|stop|restart
  $ bin/supervisorctl status           # check that pycsw is running
  $ less var/log/supervisor/pycsw.log  # check log file

Open your browser with the following URL:

.. code-block:: sh 

  http://localhost:8082/csw?service=CSW&version=2.0.2&request=GetCapabilities

