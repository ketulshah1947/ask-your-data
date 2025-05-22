FROM python:3.11-slim
WORKDIR /app
COPY ./src ./src
COPY requirements.txt .
ENV PYTHONPATH=/app
RUN pip install --no-cache-dir -r requirements.txt
# Download model only if not already present
RUN python download_model.py || echo "Model load skipped."
# Start the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]