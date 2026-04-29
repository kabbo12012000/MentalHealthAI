#!/usr/bin/env bash
set -e

export OLLAMA_HOST=0.0.0.0:11434

ollama serve > /tmp/ollama.log 2>&1 &

for i in {1..30}; do
  if curl -fsS http://localhost:11434/api/tags > /dev/null; then
    break
  fi
  sleep 1
done

ollama pull "${OLLAMA_MODEL:-llama3}"
ollama pull "${OLLAMA_EMBED_MODEL:-nomic-embed-text}"

streamlit run src/app.py \
  --server.port "${STREAMLIT_SERVER_PORT:-8501}" \
  --server.address 0.0.0.0
