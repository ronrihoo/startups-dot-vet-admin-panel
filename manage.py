from admin_panel import app, db
from admin_panel.models import User
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)


@manager.command
def init_db():
    db.create_all()
    db.session.add(User(username="admin", password='admin_pass',  email=""))
    db.session.commit()
    print('Database initialized.')


@manager.command
def drop_db():
    if prompt_bool('All data will be lost. Proceed?'):
        db.drop_all()
        print('Database has been dropped.')


if __name__ == '__main__':
    manager.run()
