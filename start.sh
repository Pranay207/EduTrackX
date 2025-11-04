#!/bin/bash

cd backend && python run.py &
BACKEND_PID=$!

cd frontend && npm run dev &
FRONTEND_PID=$!

wait $FRONTEND_PID $BACKEND_PID
