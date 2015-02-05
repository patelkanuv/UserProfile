#!/usr/bin/env python
import os

from app import create_app, db
from app.models.user import User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    from coverage import coverage
    # Track Code Coverage Report
    #cov = coverage(branch = True, omit = ['/home/kanu/Python/venv/*', 'tests/*'])
    cov = coverage(branch = True, include = ['app/*', 'lib/*'])
    cov.start()

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    # Display the Code Coverage Report
    cov.stop()
    # I'm not currently saving the report, but I can change my mind in the future
    #cov.save()
    
    print "\n\nCoverage Report:\n"
    cov.report()
    
    # I'm also not currently using the HTML version, but may want to later
    #print "HTML version: " + os.path.join(basedir, 'tmp/coverage/index.html')
    #cov.html_report(directory='tmp/coverage')
    cov.erase()
    
if __name__ == '__main__':
    manager.run()