#!flask/bin/python
from app import create_app

"""The app module, containing the app factory function."""

application = create_app()
if __name__ == "__main__":
    print("running")
    print(application.debug)
    application.run()
