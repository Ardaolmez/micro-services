# ----------------------------
# Stage 1: Build dependencies
# ----------------------------
    FROM python:3.10-slim AS builder

    WORKDIR /install
    
    # Copy only requirements and install dependencies to a temp location
    COPY requirements.txt .
    RUN pip install --prefix=/install/deps --no-cache-dir -r requirements.txt
    
    # -----------------------
    # Stage 2: Final container
    # -----------------------
    FROM python:3.10-slim
    
    # Create a non-root user named arda
    RUN adduser --disabled-password --gecos "" arda
    
    # Set working directory
    WORKDIR /home/arda/app
    
    # Copy installed dependencies from the builder image
    COPY --from=builder /install/deps /usr/local
    
    # Copy your actual app code
    COPY . .
    
    # Ensure proper ownership
    RUN chown -R arda:arda /home/arda
    
    # Switch to the non-root user
    USER arda
    
    # Expose the correct port
    EXPOSE 5003
    
    # Command to run your Flask app
    CMD ["python", "app.py"]
    

