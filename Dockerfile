#Deriving the latest base image
# FROM python:latest
# FROM continuumio/anaconda3:4.14.0
FROM continuumio/miniconda3:latest
# RUN echo conda --version

# Set the working directory inside the container
WORKDIR /app

#Labels as key value pair
LABEL Maintainer="Joel Choo"

# Copy the requirements file into the container
COPY environment.yml .

# Install the Python dependencies and activate environment
RUN conda env create --file environment.yml

# Adjust the path to point to the new environment's binaries
ENV PATH /opt/conda/envs/thematic-analysis-dev/bin:$PATH

# Download the spacy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code into the container
COPY . .

# Change the working directory to /app/src
WORKDIR /app/src

# Command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]