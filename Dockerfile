
FROM python:3
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

FROM postgres:10

# Install PostGIS packages
RUN apt-get update
RUN apt-get install --no-install-recommends --yes \
    postgresql-10-postgis-2.4 postgresql-10-postgis-2.4-scripts postgresql-contrib