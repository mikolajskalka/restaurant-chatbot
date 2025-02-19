# Restaurant Chatbot Assistant

A Discord chatbot built with Rasa and Python for handling restaurant orders and inquiries. This project was developed as part of the Scripting Languages course at [Your University Name].

## Project Overview

This chatbot can:
- Show restaurant menu
- Take orders
- Provide information about opening hours
- Check if the restaurant is open
- Handle basic conversation flows
- Provide order status updates

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Discord account and bot token
- macOS (for other operating systems, commands may vary)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python_chatbot
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Then edit `.env` file and add your Discord bot token:
```
DISCORD_TOKEN=your_discord_bot_token_here
```

## Project Structure

```
python_chatbot/
├── actions/             # Custom Rasa actions
│   └── actions.py
├── data/               # Training data
│   └── nlu.yml        # Natural Language Understanding data
├── models/            # Trained Rasa models
├── logs/              # Log files
├── main.py            # Discord bot implementation
├── endpoints.yml      # Endpoint configurations
├── credentials.yml    # Bot credentials
├── config.yml         # Rasa configuration
├── domain.yml         # Bot domain specification
└── run_bot.sh        # Script to run all services
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

## Contributing

This is a university project developed for educational purposes. If you'd like to contribute, please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Authors

[Your Name]
[Your University]
[Course Name]

## License

This project is licensed under the MIT License - see the LICENSE file for details.