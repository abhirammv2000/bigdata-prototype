from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


# ── LLM Provider ──────────────────────────────────────────

def get_llm_provider() -> str:
    """
    Supported:
      - ollama  -> local development
      - vertex  -> GCP deployment (Google Gemini)
    """
    return os.getenv("LLM_PROVIDER", "ollama").strip().lower()

def get_ollama_base_url() -> str:
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()

def get_ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3.2:1b").strip()

def get_vertex_project_id() -> str:
    # Accept either VERTEX_PROJECT_ID or the standard GOOGLE_CLOUD_PROJECT
    return (
        os.getenv("VERTEX_PROJECT_ID", "").strip()
        or os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    )

def get_vertex_location() -> str:
    return os.getenv("VERTEX_LOCATION", "us-central1").strip()

def get_vertex_model() -> str:
    return os.getenv("VERTEX_MODEL", "gemini-2.5-flash").strip()


# ── Vector Store (ChromaDB) ───────────────────────────────

def get_chromadb_host() -> str:
    return os.getenv("CHROMADB_HOST", "localhost").strip()


def get_chromadb_port() -> int:
    return int(os.getenv("CHROMADB_PORT", "8100"))


def get_chromadb_persist_dir() -> str:
    return os.getenv("CHROMADB_PERSIST_DIR", os.path.join(_workspace_root(), ".chromadb"))


def get_chromadb_mode() -> str:
    return os.getenv("CHROMADB_MODE", "local").strip().lower()


# ── Marquez / OpenLineage ─────────────────────────────────

def get_marquez_url() -> str:
    return os.getenv("MARQUEZ_URL", "").strip()


# ── Airflow / Composer ────────────────────────────────────

def get_airflow_base_url() -> str:
    return os.getenv("AIRFLOW_BASE_URL", "").strip()


# ── Storage ───────────────────────────────────────────────

def get_gcs_data_bucket() -> str:
    return os.getenv("GCS_DATA_BUCKET", "").strip()


# ── Embeddings ────────────────────────────────────────────

def get_embedding_model_name() -> str:
    return os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2").strip()


# ── Helpers ───────────────────────────────────────────────

def _workspace_root() -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))
