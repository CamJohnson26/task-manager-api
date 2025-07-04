# Task Manager API

## Description
Backend for task manager, Visualize recurring, one off, and event tasks on a single 2d view, with priority of the tasks represented by transparency and size.

## Usage instructions
```shell
pip3 install -r requirements.txt
gunicorn --worker-tmp-dir /dev/shm api:app
```
Then connect to the API at `http://localhost:8000`.

## Technical details
* This is a Flask app that uses Gunicorn as the WSGI server.