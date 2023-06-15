import os
import time

import app


def init_db():
    app.db.create_all()

    for i in ["Alice", "Bob"]:
        user = app.User(name=i)
        app.db.session.add(user)

    app.db.session.commit()


if __name__ == "__main__":
    time.sleep(10)
    with app.app.context():
        init_db()
