#!/usr/bin/env bash
# Transcribe one finished turn over a single HTTP request with the Sync API.
# Usage: ./sync_turn.sh turn.wav
set -euo pipefail
curl -X POST https://sync.assemblyai.com/v1/transcribe \
  -H "Authorization: ${ASSEMBLYAI_API_KEY}" \
  -H 'X-AAI-Model: universal-3-6-pro' \
  -F "audio=@${1:-turn.wav};type=audio/wav"
