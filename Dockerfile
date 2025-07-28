FROM python:3.11-alpine

# Install system dependencies
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    bash \
    ttf-freefont \
    dumb-init \
    curl

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Create non-root user
RUN adduser -D appuser
USER appuser

# Set working directory
WORKDIR /home/appuser

# Copy script into container
COPY obfuscate_browsing.py .

# Install Python dependencies
RUN pip install --no-cache-dir selenium

# Run the script using dumb-init for signal handling
ENTRYPOINT ["dumb-init", "python", "obfuscate_browsing.py"]
