# Grab the Docker Image
FROM python:3.9.7

# set the working directory
WORKDIR /usr/src/app

# copy the requirements file to dir
COPY requirements.txt ./

# run the reqs file
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files 
# The order of the copying of the files are important for optimization
COPY . . 

# command to start our app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]