FROM python:3.8

WORKDIR /code

# Install dependencies
RUN pip install .


# Define the Docker image's behavior at runtime
CMD ["python3", "-m", "unittest", "wpscraper]

