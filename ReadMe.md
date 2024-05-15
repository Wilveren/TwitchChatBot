# Python Twitch Chatbot

A Chat Bot for Twitch built in Python. Contains functionality to respond to various commands, including posting random lines from an external text file, 
and optionally generating responses via ChatGPT.

Current Version: 0.3.0

## Requirements

- A secondary Twitch account that your bot will post as that is separate from the channel you stream to.
- An account and org setup with [Open AI](https://platform.openai.com/overview), if you plan to use the ChatGPT Integration.
- Install the DadJoke and irc external libraries using pip: 
`pip install irc`
`pip install dadjokes`
`pip install openai`
- You will need an OAuth token for the account of your Twitch Chatbot. Refer to [Twitch Developer Documentation](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) for info on how to get this.
- You will need an API Key from your Open AI account if you plan to use the ChatGPT integration. You can find this in the API key page of your account.

## Setup

Fill in the values in `variables.py` with the relevant pieces of information. Bear in mine that your Twitch OAuth Token and OpenAI Key should be kept secret.
**Do not share these with anyone.**
To use the `!lore` command, customize the `lore.txt` file with the text you would like this command to return. Each potential response should be on a single line, and 
less than 500 characters. 
Customize the `timed_message` function with whatever message you would like to be periodically posted into chat, such as a discord channel invitation. You can also adjust 
the period of time between posts, and how many other messages should have been posted before it will post again. This will prevent your chat being spammed by this message.

```python
def timed_message():
    global message_count
    while True:
        #Posts a set message every 10 minutes, but only if at least 5 other messages have been posted in chat since the last time this was posted
        if message_count > 5:
            message_count = 0
            send_message("") # Your Message inside these quotes
        time.sleep(600) # Amount of time in seconds to wait before posting again
```

If using ChatGPT integration, fill in the `content` under `"role": "system",` in `generate_response` with any background information you want the bot to have, such as
its temperment.

```python
def generate_response(username, message):
    # Generate a response using ChatGPT

    # Retrieve user's context
    global user_context
    context = user_context.get(username, [])

    context.append(message)

    response = Openai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        n = 1,
        messages=[
        { 
          "role": "system", 
          # Use this to help fine-tune the responses you receieve. You can establish the personality of the bot, any self-identifying info you want it to have, and message format.
          "content": "You are a Twitch chatbot, and should respond in a friendly, informative way. Summarize to keep responses brief."
        },
...
```

For the `!discord` command, fill in the `send_message` function call of this command with the link to your discord, along with any message you want posted.

```python
...
    elif message.startswith('!discord'):
        # Respond with a message containing discord invite
        send_message(" ") # your message and discord invite link go inside these quotes.
...
```

To activate the bot, run the `Chatbot.py` file locally from VScode or any other editor that supports python. The bot will immediately being listening for messages in your
Twitch channel, respond to commands, and begin posting your timed message according to your settings.

## Commands

- !hello: Greets the user.
- !commands: Displays a list of available commands.
- !dadjoke: Shares a dad joke.
- !roll6: Rolls a six-sided die.
- !roll20: Rolls a twenty-sided die.
- !lurk: Acknowledges a user who is lurking.
- !lore: Shares a random piece of lore from the mega_lore.txt file.
- !herald [message]: Generates a response using the ChatGPT model. Only available if OpenAI credentials are provided.
- !setdeath [number]: Manually sets the death counter. Only accessible by the broadcaster or moderators.
- !death: Increases the death counter by 1 and acknowledges a death. Only accessible by the broadcaster or moderators.
- !dcount: Displays the current death counter.
- !discord: Posts an invitation to a given discord channel, with accompanying message.
