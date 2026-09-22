import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import ALLOWED_ORIGINS, APP_DESCRIPTION, APP_TITLE, APP_VERSION
from backend.api.routes import router

logger=logging.getLogger('ats_resume_scorer')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Models are intentionally NOT loaded here ──────────────────────────────
    # Loading SpaCy + SentenceTransformer at boot exceeds Render's 512 MB free
    # tier and crashes the process before a single request is served.
    # Instead, backend/utils/model_loader.py provides lru_cache singletons that
    # load each model once on the first request that needs it.
    # The first resume-analysis call will be ~5 s slower; all subsequent calls
    # use the cached model and are fast.
    logger.info("ATS Resume Analyzer API starting (models will load lazily on first request).")
    yield
    logger.info("Shutting down the ATS Resume Analyzer API.")

app=FastAPI(
    title=APP_TITLE, 
    description=APP_DESCRIPTION, 
    version=APP_VERSION, 
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True, 
    allow_methods     = ['*'],
    allow_headers     = ['*'],

)

app.include_router(router)

@app.get('/')
async def root():
    return {
        'name':      'ATS Resume Analyzer API',
        'version':   '2.0.0',
        'endpoints': {
            'POST   /api/v1/analyze-resume': 'Analyze a resume',
            'GET    /api/v1/history':        'Get user history',
            'DELETE /api/v1/history/:id':    'Delete a history entry',
            'GET    /api/v1/health':         'Health check',
            'POST   /api/v1/generate-pdf':   'Generate PDF report from data',
        },
    }

if __name__=='__main__':
    import uvicorn
    uvicorn.run(
        'backend.main:app',
        host    = '0.0.0.0',
        port    = 8000,
        reload  = True,    # Auto-restart on code changes (dev only)
    )
