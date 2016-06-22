import multiprocessing

#bind = 'unix://${prefix}/var/run/${name}.socket'
bind = '127.0.0.1:9201'
workers = multiprocessing.cpu_count() * 2 + 1

# environment
raw_env = ["HOME=${lib_directory}", 
           "PYCSW_CONFIG=${etc_directory}/${name}.cfg", 
           "PATH=${env_path}/bin:/usr/bin:/bin", 
           ]                                                                                                               

# logging

debug = True
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
