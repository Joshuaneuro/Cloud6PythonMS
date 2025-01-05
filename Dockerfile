FROM python:3.10.7
WORKDIR /app/test

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["languageApp", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]