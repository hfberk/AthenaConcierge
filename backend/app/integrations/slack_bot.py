from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(token=settings.SLACK_BOT_TOKEN)

@app.message("")
def handle_message(message, say, logger):
    """Handle all messages"""
    text = message.get("text", "")
    user = message.get("user")
    
    logger.info(f"Received message from {user}: {text}")
    
    # Simple echo for now
    say(f"Message received: {text}")

def start_slack_bot():
    """Start the Slack bot in Socket Mode"""
    handler = SocketModeHandler(app, settings.SLACK_APP_TOKEN)
    logger.info("Starting Slack bot...")
    handler.start()

if __name__ == "__main__":
    start_slack_bot()
