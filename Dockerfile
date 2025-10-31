FROM python:3.13-slim


# Create base working directory inside the container
WORKDIR /app

# Copy requirements file from your Backend folder
COPY requirements.txt ./Backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r Backend/requirements.txt

# Copy entire Backend folder to /app/Backend inside container
COPY . /app



# Expose the FastAPI port
EXPOSE 8000