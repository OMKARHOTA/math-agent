FROM python:3.13-slim


# Create base working directory inside the container
WORKDIR /app

# Copy requirements file from your Backend folder
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire Backend folder to /app/Backend inside container
COPY . /app



# Expose the FastAPI port
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
