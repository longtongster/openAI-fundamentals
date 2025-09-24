# Start from the full Python base image (not slim)
FROM python:3.10

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir \
    crewai \
    crewai-tools \
    pandas \
    scikit-learn

# Copy your application code (if any)
COPY . .

# Keep container running so code can be executed inside it
# CMD ["tail", "-f", "/dev/null"]