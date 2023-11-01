FROM python:3.9-bullseye

WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the application
ENTRYPOINT [ "bash", "neuropulse" , "config.yaml"]
