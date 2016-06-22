# -*- coding: utf-8 -*-

"""Buildout Recipe pycsw"""

import os
import logging
from mako.template import Template

import zc.recipe.deployment
from birdhousebuilder.recipe import conda, supervisor, nginx

templ_pycsw = Template(filename=os.path.join(os.path.dirname(__file__), "pycsw.cfg"))
templ_app = Template(filename=os.path.join(os.path.dirname(__file__), "cswapp.py"))
templ_gunicorn = Template(filename=os.path.join(os.path.dirname(__file__), "gunicorn.conf.py"))
templ_cmd = Template(
    "${env_path}/bin/gunicorn -c ${etc_directory}/gunicorn.${name}.py cswapp:app")

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs a pycsw catalog service instance."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.name = options.get('name', name)
        self.options['name'] = self.name

        self.logger = logging.getLogger(self.name)

        deployment = zc.recipe.deployment.Install(buildout, "pycsw", {
                                                'prefix': self.options['prefix'],
                                                'user': self.options['user'],
                                                'etc-user': self.options['user']})
        deployment.install()

        self.options['etc-prefix'] = deployment.options['etc-prefix']
        self.options['var-prefix'] = deployment.options['var-prefix']
        self.options['etc-directory'] = self.options['etc_directory'] = deployment.options['etc-directory']
        self.options['lib-directory'] = self.options['lib_directory'] = deployment.options['lib-directory']
        self.options['log-directory'] = self.options['log_directory'] = deployment.options['log-directory']
        self.prefix = self.options['prefix']

        self.env_path = conda.conda_env_path(buildout, options)
        self.options['env_path'] = self.env_path
        
        self.hostname = options.get('hostname', 'localhost')
        self.options['hostname'] = self.hostname

        self.port = options.get('port', '8082')
        self.options['port'] = self.port

        self.options['transactions'] = options.get('transactions', 'true')
        self.options['allowed_ips'] = options.get('allowed_ips', '127.0.0.1')

        self.options['loglevel'] = options.get('loglevel', 'DEBUG')

        self.bin_dir = b_options.get('bin-directory')

    def install(self, update=False):
        installed = []
        installed += list(self.install_pycsw(update))
        installed += list(self.install_config())
        installed += list(self.install_app())
        installed += list(self.setup_db())
        installed += list(self.install_gunicorn())
        installed += list(self.install_supervisor(update))
        installed += list(self.install_nginx(update))
        return installed

    def install_pycsw(self, update):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'pycsw<2 geolinks<0.2 gunicorn', 'channels': 'ioos birdhouse'})
        return script.install(update=update)
        
    def install_config(self):
        """
        install pycsw config in etc/pycsw
        """
        result = templ_pycsw.render(**self.options)
        output = os.path.join(self.options['etc-directory'], self.name+'.cfg')

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_gunicorn(self):
        """
        install gunicorn conf in etc/pycsw
        """
        result = templ_gunicorn.render(**self.options)
        output = os.path.join(self.options['etc-directory'], 'gunicorn.'+self.name+'.py')

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_app(self):
        """
        install etc/cswapp.py
        """
        result = templ_app.render(prefix=self.prefix,)
        output = os.path.join(self.options['etc-directory'], 'cswapp.py')

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def setup_db(self):
        """
        setups initial database as configured in default.cfg
        """
        
        output = os.path.join(self.options['lib-directory'], self.name, 'data', 'records.db')
        if os.path.exists(output):
            return []
        
        make_dirs(os.path.dirname(output))
        
        from subprocess import check_call
        cmd = [os.path.join(self.env_path, 'bin/pycsw-admin.py')]
        cmd.extend(["-c", "setup_db"])
        cmd.extend(["-f", os.path.join(self.options["etc-directory"], self.name+".cfg")])
        check_call(cmd)
        return []
        
    def install_supervisor(self, update=False):
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'program': self.name,
             'command': templ_cmd.render(**self.options),
             'directory': self.options['etc-directory']
             })
        return script.install(update)

    def install_nginx(self, update=False):
        script = nginx.Recipe(
            self.buildout,
            self.name,
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'input': os.path.join(os.path.dirname(__file__), "nginx.conf"),
             'port': self.port,
             'hostname': self.options.get('hostname'),
             })
        return script.install(update=update)
        
    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

