bind = 'unix://${prefix}/var/run/pycsw_${sites}.socket'
workers = 3

# environment
raw_env = ["HOME=${prefix}/var/lib/pycsw", 
           "PYCSW_CONFIG=${prefix}/etc/pycsw/${sites}.cfg", 
           "PATH=${prefix}/bin:/usr/bin:/bin", 
           ]                                                                                                               

# logging

debug = True
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
