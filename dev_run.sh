#!/bin/bash

gnome-terminal -- bash -c "
cd \"$(pwd)\";
source .venv/bin/activate;
uvicorn backend.main:app --reload &
cd frontend;
npm run dev &
wait;
exec bash"