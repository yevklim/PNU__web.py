#!./.env/bin/python
from app import create_app

if __name__ == '__main__':
    create_app("dev").run(debug=True)
