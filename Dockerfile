FROM python:3.9

WORKDIR /metaland-accounts

# First, copy requirements.txt to app directory
COPY requirements.txt .

# Run pip install to install all dependencies
# (this job will cached, if requirements.txt was not changed)
RUN pip install -r requirements.txt

# Copy source code files to app directory
# (except files on .dockerignore)
COPY . .

EXPOSE 8000

# Add --proxy-headers to trust proxy like Nginx or Traefik.
CMD ["uvicorn", "mtl_accounts.main:app", "--host", "0.0.0.0", "--port", "8000"]