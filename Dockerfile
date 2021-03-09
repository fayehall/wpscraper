FROM python:3


# Install dependencies
RUN pip install .


# Define the Docker image's behavior at runtime
CMD ["python3", "-m", "unittest", "wpscraper]

