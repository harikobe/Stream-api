FROM python:3

ENV PYTHONBUFFERED=1

#create new folder in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

#install the required libraries
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

#Run the fastapi app directly
CMD ["uvicorn", "stream_data_api:app", "--host", "0.0.0.0", "--port", "8000"]
