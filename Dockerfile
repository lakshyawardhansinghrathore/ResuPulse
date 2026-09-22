FROM python:3.11-slim

# Install system dependencies required for WeasyPrint and SpaCy
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# ── CRITICAL: Install CPU-only PyTorch FIRST ──────────────────────────────────
# sentence-transformers depends on torch. If we let pip resolve it, it pulls in
# the full CUDA build (~2 GB of nvidia_* packages) which crashes Render's 512 MB
# free tier. Installing the CPU wheel first tells pip "torch is already satisfied"
# so it won't download the GPU variant when installing sentence-transformers.
RUN pip install --no-cache-dir \
    torch==2.3.1+cpu torchvision==0.18.1+cpu torchaudio==2.3.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Copy and install remaining backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the SpaCy model
RUN python -m spacy download en_core_web_md

# Pre-download the sentence-transformer model so it's baked into the image
# (avoids a slow first-request download on Render's cold start)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the backend code
COPY backend ./backend

# Expose the FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
