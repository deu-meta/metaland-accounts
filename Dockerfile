FROM python:3.9

WORKDIR /app

# First, copy requirements.txt to app directory
COPY requirements.txt .

# Run pip install to install all dependencies
# (this job will cached, if requirements.txt was not changed)
RUN pip install -r requirements.txt

# Copy source code files to app directory
# (except files on .dockerignore)
COPY . .

EXPOSE 8000

CMD ["python", "run.py"]