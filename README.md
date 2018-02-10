### On machines with Docker and Docker Compose installed, simply run:

```
docker-compose build
docker-compose up
```

### Otherwise, you'll need to:

* install MongoDB
* change `app.py` to reference your MongoDB host and port
* install Python 3
* run `pip install -r requirements.txt`
* run `FLASK_APP=app.py flask run` to start the server

You might need to change the lines
```
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```
to something like:
```app.run(debug=True)```