# Use an official Python image as a base
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Ignore virtual environment and cache files
RUN rm -rf venv __pycache__

# Expose port 8000
EXPOSE 8000

# Run the application (modify based on your app's entry point)
CMD ["python", "app.py"]
