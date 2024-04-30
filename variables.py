# External file for sensitive variables for the Twitch Chat Bot
from openai import OpenAI

# Server to connect to. Likely will not change from "irc.chat.twitch.tv"
server = 'irc.chat.twitch.tv'
# Port to connect to and listen from
port = 6667
# Twitch channel name that your bot will post as
nickname = 
# OAuth token for your bot. Must be generated and authenticated using your bot's Twitch account, not your own
token = 
# OpenAI API key and info. Only required if you want your bot to have ChatGPT integration, which means you must create the Org and Project and setup payment plan first
Openai_client = OpenAI(
    api_key=,
    organization=,
    project=)