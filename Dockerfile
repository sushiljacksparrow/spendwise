# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN apt-get -y update && apt-get install -y libzbar-dev

# install dependencies
RUN pip install -r requirements.txt
RUN pip install tesseract

# copy the content of the local src directory to the working directory
COPY src/ .
COPY templates/ templates/

RUN ls

EXPOSE 50000

# command to run on container start
CMD [ "python", "./server.py" ]
