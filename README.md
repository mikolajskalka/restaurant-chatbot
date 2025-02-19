# Restaurant Chatbot Assistant

A Discord chatbot built with Rasa and Python for handling restaurant orders and inquiries. This project was developed as part of the Scripting Languages course at Jagiellonian University.

## Project Overview

This chatbot can:
- Show restaurant menu
- Take orders
- Provide information about opening hours
- Check if the restaurant is open
- Handle basic conversation flows
- Provide order status updates

## Prerequisites

- Python 3.10
- pip (Python package manager)
- Discord account and bot token
- macOS (for other operating systems, commands may vary)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python_chatbot
```

2. Set up environment variables in `.env` file:
```
DISCORD_TOKEN=your_discord_bot_token_here
```

3. Create and activate virtual environment or run `run_bot.sh` and it will setup everything:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Running the Bot

### Method 1: Using the run script
```bash
chmod +x run_bot.sh  # Make script executable (first time only)
./run_bot.sh
```

### Method 2: Manual startup
1. Start the Rasa server:
```bash
rasa run --enable-api --cors "*"
```

2. In a new terminal, start the Rasa Action server:
```bash
rasa run actions --cors "*"
```

3. In another terminal, start the Discord bot:
```bash
python main.py
```

## Training the Model

To retrain the Rasa model with updated data:
```bash
rasa train
```

## Available Commands

The bot understands the following intents:
- Greetings
- Menu inquiries
- Order placement
- Opening hours check
- Restaurant status check
- Order status check
- Thank you messages

## Development

To modify the bot's behavior:
1. Update intents in `data/nlu.yml`
2. Modify responses in `domain.yml`
3. Add custom actions in `actions/actions.py`
4. Retrain the model using `rasa train`

## Testing

To test the bot locally before Discord integration:
```bash
rasa shell
```

## Logs

Logs are stored in the `logs` directory:
- `rasa.log` - Rasa server logs
- `actions.log` - Action server logs
- `bot.log` - Discord bot logs
