from flask import Flask
from app.app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host='13.58.210.11', port=80)
