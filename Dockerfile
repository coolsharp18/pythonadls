FROM python:3.7

# Upgrade pip

ENV accountname=NONE
ENV accountkey=NONE
ENV filesystem=NONE

ENV LISTEN_PORT=5001
EXPOSE 5001

RUN pip install --upgrade pip



# Copy the application files
COPY ./requirements.txt /usr/src/app/
COPY ./run.py /usr/src/app/

# Set the working directory to where the application files are
WORKDIR /usr/src/app

RUN pip install --no-cache -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ pythonadls-coolsharp18==0.0.1

CMD python run.py