FROM python:3.9

RUN useradd -m backend

# set the working directory in the container
WORKDIR /home/backend

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./api ./api

# change owner of files
RUN chown -R backend:backend /home/backend

USER backend

EXPOSE 3000

CMD python3.9 -m uvicorn api:app --port 3000 --host 0.0.0.0