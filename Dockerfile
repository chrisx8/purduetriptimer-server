FROM python:3-alpine

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

# Copy code
COPY . /app/
WORKDIR /app

# Set permission
RUN chown nobody:nogroup -R /app

EXPOSE 8000
USER nobody

CMD gunicorn app:app -b 0.0.0.0:8000
