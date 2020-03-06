FROM python:3.7

# Upgrade pip

ENV accountname=NONE
ENV accountkey=NONE
ENV filesystem=NONE

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# Copy the application files
COPY . /usr/src/app/

# Set the working directory to where the application files are
WORKDIR /usr/src/app

CMD python run.py