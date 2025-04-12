# ----------------------------
# Stage 1: Build dependencies
# ----------------------------
    FROM python:3.10-slim AS builder

    WORKDIR /install
    
    COPY requirements.txt .
    RUN pip install --prefix=/install/deps --no-cache-dir -r requirements.txt
    
    # -----------------------
    # Stage 2: Final container
    # -----------------------
    FROM python:3.10-slim
    
    # Create a non-root user
    RUN adduser --disabled-password --gecos "" arda
    
    # Set working directory
    WORKDIR /home/arda/app
    
    # Create the /app/instance directory and set permissions
    RUN mkdir -p /home/arda/app/instance && chown -R arda:arda /home/arda/app
    
    # Copy installed dependencies
    COPY --from=builder /install/deps /usr/local
    
    # Copy application code
    COPY . .
    
    # Ensure ownership for everything under /home/arda
    RUN chown -R arda:arda /home/arda
    
    # Switch to non-root user
    USER arda
    
    # Expose app port
    EXPOSE 5004
    
    # Run the Flask app
    CMD ["python", "app.py"]
    