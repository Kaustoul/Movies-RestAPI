# Movies REST API
A simple Movies FLASK API with sqlite database

## Requirements

- Python 3.10.12

## How to run the app

Download dependencies:      

    $ pip install -r requirements.txt

To run the app you can use the `run` script. You will need to give it permission to run:

    $ chmod 755 ./run

And then you are ready to run the app:

    $ ./run

## How to test the app

- With the app running you can try out API requests with the address in the app output (e.g with postman).

- You can run unit tests located in the test.py file:

      $ python3 test.py


## Using docker

Building the image:

    $ docker build -t movies-restapi:1.0 .

And running the container:

    $ docker run -p 5000:5000 movies-restapi:1.0
