activate_this = '/var/www/UserProfile/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import os
import sys

sys.path.append('/var/www/UserProfile/')
os.environ['PYTHON_EGG_CACHE'] = '/var/www/UserProfile/.user_profile_egg_cache' 
sys.stdout = sys.stderr

print sys.path

from manage import app as application
