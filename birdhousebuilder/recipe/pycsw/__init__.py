# -*- coding: utf-8 -*-

"""Buildout Recipe pycsw"""

import os
from mako.template import Template

from birdhousebuilder.recipe import conda, supervisor, nginx

templ_pycsw = Template(filename=os.path.join(os.path.dirname(__file__), "pycsw.cfg"))
templ_app = Template(filename=os.path.join(os.path.dirname(__file__), "cswapp.py"))
templ_gunicorn = Template(filename=os.path.join(os.path.dirname(__file__), "gunicorn.conf.py"))
templ_cmd = Template(
    "${prefix}/bin/gunicorn -c ${prefix}/etc/pycsw/gunicorn.${sites}.py cswapp:app")

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs a pycsw catalog service instance."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.prefix = options.get('prefix', conda.prefix())
        self.options['prefix'] = self.prefix
        
        self.sites = options.get('sites', self.name)
        self.options['sites'] = self.sites
        self.options['prefix'] = self.prefix
        self.hostname = options.get('hostname', 'localhost')
        self.options['hostname'] = self.hostname
        self.options['user'] = options.get('user', '')

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
        
        mypath = os.path.join(self.prefix, 'var', 'lib', 'pycsw')
        conda.makedirs(mypath)
        
        mypath = os.path.join(self.prefix, 'var', 'log', 'pycsw')
        conda.makedirs(mypath)

        if update == True:
            return script.update()
        else:
            return script.install()
        
    def install_config(self):
        """
        install pycsw config in etc/pycsw
        """
        result = templ_pycsw.render(**self.options)
        output = os.path.join(self.prefix, 'etc', 'pycsw', self.sites+'.cfg')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_gunicorn(self):
        """
        install gunicorn conf in etc/pycsw
        """
        result = templ_gunicorn.render(**self.options)
        output = os.path.join(self.prefix, 'etc', 'pycsw', 'gunicorn.'+self.sites+'.py')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_app(self):
        """
        install etc/cswapp.py
        """
        result = templ_app.render(
            prefix=self.prefix,
            )
        output = os.path.join(self.prefix, 'etc', 'pycsw', 'cswapp.py')
        conda.makedirs(os.path.dirname(output))
                
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def setup_db(self):
        """
        setups initial database as configured in default.cfg
        """
        
        output = os.path.join(self.prefix, 'var', 'lib', 'pycsw', self.sites, 'data', 'records.db')
        if os.path.exists(output):
            return []
        
        conda.makedirs(os.path.dirname(output))
        
        from subprocess import check_call
        cmd = [os.path.join(self.prefix, 'bin/pycsw-admin.py')]
        cmd.extend(["-c", "setup_db"])
        cmd.extend(["-f", os.path.join(self.prefix, "etc", "pycsw", self.sites+".cfg")])
        check_call(cmd)
        return []
        
    def install_supervisor(self, update=False):
        script = supervisor.Recipe(
            self.buildout,
            self.sites,
            {'user': self.options.get('user'),
             'program': self.sites,
             'command': templ_cmd.render(**self.options),
             'directory': os.path.join(self.prefix, 'etc', 'pycsw')
             })
        return script.install(update)

    def install_nginx(self, update=False):
        script = nginx.Recipe(
            self.buildout,
            self.name,
            {'input': os.path.join(os.path.dirname(__file__), "nginx.conf"),
             'user': self.options.get('user'),
             'sites': self.sites,
             'prefix': self.prefix,
             'port': self.port,
             'hostname': self.options.get('hostname'),
             })
        if update==True:
            return script.update()
        else:
            return script.install()
        
    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

