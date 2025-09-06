#Use an official Python runtime as a parent image 
FROM python:3.11-slim

#Set the working directory in the container
WORKDIR /app

#Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Install Jupyter Notebook
RUN pip install jupyter notebook

#Make port 8888 aviable to the orld outside this container
EXPOSE 8888

#Run a Jupyter notebook server when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

