FROM python:3.11-slim

ENV GROUP_ID=1000 \
    USER_ID=1000

# Create app folder
RUN mkdir -p /backend/app

# Copy app
ADD app/* /backend/app/
ADD templates/* /templates/
COPY wsgi.py /backend/wsgi.py
COPY requirements.txt /backend/requirements.txt

WORKDIR /backend/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

RUN addgroup --gid $GROUP_ID www
RUN adduser --shell /bin/sh -u $USER_ID www --ingroup www

USER www

# Run the application
CMD ["gunicorn", "-w", "1", "--reload", "--bind", "0.0.0.0:5000", "wsgi"]