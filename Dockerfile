# base image
FROM python:3.8-slim-buster
WORKDIR /taskmanagerpro
# COPY your application files
COPY requirements.txt requirements.txt
COPY ./taskpro ././taskpro
COPY ./templates ././templates
COPY ./static ././static
COPY . .
# Install or upgrade pip and install requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
# Start your application, binding it to 0.0.0.0 to make it accessible externally
CMD [ "python3", "app.py", "--host", "0.0.0.0" ]