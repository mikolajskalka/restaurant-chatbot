import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
import asyncio
import logging
import yaml

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load Rasa model
try:
    model_path = "models/20250218-235416-tiny-conduit.tar.gz"
    
    # Load endpoints from yaml file
    with open("endpoints.yml", "r") as f:
        endpoints = yaml.safe_load(f)
    
    # Create endpoint config
    action_endpoint = EndpointConfig(
        endpoints["action_endpoint"]["url"]
    )
    
    # Load agent with proper endpoint configuration
    agent = Agent.load(
        model_path,
        action_endpoint=action_endpoint
    )
    
    logger.info(f"Successfully loaded Rasa model from {model_path}")
except Exception as e:
    logger.error(f"Failed to load Rasa model: {str(e)}")
    raise SystemExit("Could not load Rasa model. Exiting.")


async def get_rasa_response(message_text, sender_id):
    """Async function to get response from Rasa"""
    loop = asyncio.get_event_loop()
    responses = await agent.handle_text(
        text_message=message_text,
        sender_id=sender_id
    )
    return responses

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    try:
        # Log incoming message
        logger.debug(f"Received message: {message.content}")
        
        # Use sender's ID to maintain conversation state
        sender_id = str(message.author.id)
        
        # Get response from Rasa
        responses = await get_rasa_response(message.content, sender_id)
        
        # Handle Rasa response
        if responses:
            logger.debug(f"Rasa responses: {responses}")
            for response in responses:
                if isinstance(response, dict) and 'text' in response:
                    await message.channel.send(response['text'])
                    logger.debug(f"Sent response: {response['text']}")
        else:
            logger.warning(f"No response received from Rasa for message: {message.content}")
            await message.channel.send("I'm not sure how to respond to that.")
            
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        await message.channel.send("I'm having trouble understanding that right now.")

# Run the bot
bot.run(TOKEN)