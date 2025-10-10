FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

# Install Alpine packages needed for building dependencies and libgcc
RUN apk add --no-cache libgcc build-base

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


