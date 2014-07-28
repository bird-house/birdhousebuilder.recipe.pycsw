bind = 'unix://${prefix}/var/run/${sites}.socket'
workers = 3

# environment
raw_env = ["HOME=${prefix}/var/lib/pycsw", 
           "PYCSW_CFG=${prefix}/etc/pycsw/${sites}.cfg", 
           "PATH=${bin_dir}:${prefix}/bin:/usr/bin:/bin", 
           ]                                                                                                               

# logging

debug = True
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
