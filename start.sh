#!/usr/bin/env bash
set -e

export OLLAMA_HOST=127.0.0.1:11434

ollama serve > /tmp/ollama.log 2>&1 &

for i in {1..30}; do
  if curl -fsS http://localhost:11434/api/tags > /dev/null; then
    break
  fi
  sleep 1
done

# Pull models in background so the UI can start quickly.
(
  ollama pull "${OLLAMA_MODEL:-llama3}"
  ollama pull "${OLLAMA_EMBED_MODEL:-nomic-embed-text}"
) &

streamlit run src/app.py \
  --server.port "${PORT:-${STREAMLIT_SERVER_PORT:-8501}}" \
  --server.address 0.0.0.0
