# set base image
FROM python:3.7

# create service directory
WORKDIR /usr/linguicator/linguicator-predictor

# install poetry
RUN pip install poetry

# copy dependency files
COPY poetry.lock ./
COPY pyproject.toml ./

# install dependencies
RUN poetry install

# copy all files
COPY . .

# expose websocket port
EXPOSE 8765

# start server
ENTRYPOINT ["poetry", "run", "linguicator"]
