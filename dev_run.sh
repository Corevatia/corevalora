#!/bin/bash
set -e

docker context use desktop-linux
docker compose up -d db

gnome-terminal -- bash -lic "
cd backend
source .venv/bin/activate
uvicorn main:app --reload &
cd ../frontend
npm run dev &
wait
exec bash
"
