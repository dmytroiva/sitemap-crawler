# Stage 1: Build dependencies
FROM python:3.9-slim AS builder

# Copy the requirements file to the /app directory
COPY ./scripts/utils/requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --user -r /app/requirements.txt

# Stage 2: Final image
FROM python:3.9-slim

# Copy the installed dependencies from the builder stage to the final image
COPY --from=builder /root/.local /root/.local

# Copy the necessary files to the /app directory
COPY ./scripts/utils/sitemap_crawler_v6.1.py /app/sitemap_crawler_v6.1.py
COPY ./scripts/utils/domain.txt /app/data/domain.txt

# Set the working directory
WORKDIR /app

# Add the local bin directory to the PATH
ENV PATH=/root/.local/bin:$PATH

# Set the entrypoint command to run the script
ENTRYPOINT ["python", "sitemap_crawler_v6.1.py"]
