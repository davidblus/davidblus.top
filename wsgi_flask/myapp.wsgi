# -*- coding:utf-8 -*-
# log directory : /var/log/apache2/error.log

activate_this = '/home/ubuntu/python_virtual_env/python3_env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/html/wsgi_flask')

from index import app as application
