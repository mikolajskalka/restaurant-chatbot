#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
pip install -r requirements.txt

# Function to kill processes on exit
cleanup() {
    echo -e "${RED}Shutting down services...${NC}"
    kill $RASA_PID $ACTION_PID $BOT_PID 2>/dev/null
    exit
}

# Set up trap for cleanup
trap cleanup EXIT

# Start Rasa server
echo -e "${GREEN}Starting Rasa server...${NC}"
rasa run --enable-api --cors "*" > logs/rasa.log 2>&1 &
RASA_PID=$!

# Wait for Rasa server to start
sleep 5

# Start Rasa Action server
echo -e "${GREEN}Starting Rasa Action server...${NC}"
rasa run actions --cors "*" > logs/actions.log 2>&1 &
ACTION_PID=$!

# Wait for Action server to start
sleep 5

# Start Discord bot
echo -e "${GREEN}Starting Discord bot...${NC}"
python main.py > logs/bot.log 2>&1 &
BOT_PID=$!

# Create logs directory if it doesn't exist
mkdir -p logs

echo -e "${GREEN}All services are running!${NC}"
echo -e "Rasa server PID: $RASA_PID"
echo -e "Action server PID: $ACTION_PID"
echo -e "Discord bot PID: $BOT_PID"
echo -e "${BLUE}Logs are available in the logs directory${NC}"
echo -e "${BLUE}Press Ctrl+C to stop all services${NC}"

# Wait for Ctrl+C
wait
