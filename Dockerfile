FROM python:3.6

RUN mkdir -p /opt/services/cactus/src
WORKDIR /opt/services/cactus/src


COPY . /opt/services/cactus/src

RUN pip3 install -r requirements.txt
RUN cd cactus  && python3 manage.py collectstatic --no-input 

