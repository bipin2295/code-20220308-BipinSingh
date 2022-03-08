##########################################################################################################################
#															 #
# Usage: docker build -t <repo>/<image_name>:<tag_name> -f <Dockerfile> .                				 #
#															 #
# Example: docker build -t bipin2295/bmi_app:v1.0 -f Dockerfile .         						 #
# Running: docker run bipin2295/bmi_app:v1.0 										 #
##########################################################################################################################

FROM python:3.9-slim-buster 

LABEL version="1.0"
LABEL author="Bipin Singh <bipin2295@gmail.com>"

# make the working directory in the container
RUN mkdir /app

# specify where to install the app
WORKDIR /app/

# add all files to the working directory
ADD . /app/

# Install the dependencies in the requirements file.
RUN pip install -r requirements.txt

CMD ["python", "/app/src.py"]

