import irc.client
from dadjokes import Dadjoke
import random
import time
import threading
import re
import variables

channel = variables.channel
server = variables.server
port = variables.port
nickname = variables.nickname
token = variables.token
Openai_client = variables.Openai_client if variables.Openai_client else None
message_count = 0
names = []
counter = 0

# Opens an external text file, reads it, and stores the information in a list
with open('mega_lore.txt', 'r') as file:
    lore = file.read()
    lore = lore.splitlines()

# Function to send messages to the Twitch chat
def send_message(message):
    c.privmsg(f'#{channel}', message)

# Function to handle the welcome message when the bot connects to your channel
def on_welcome(connection, event):
    connection.join(f'#{channel}')
    print("Connected to Twitch IRC server")

# Function to handle errors
def on_error(connection, event):
    print("Error:", event.arguments)

    c.add_global_handler('error', on_error)

# Function to handle incoming messages
def on_pubmsg(connection, event):
    print("Message received")
    global message_count 
    global names
    global counter
    message_count = message_count+1
    message = event.arguments[0].lower().strip()
    username = event.source.nick
    tags = event.tags



# Function to check if the user has a specific role
    def has_role(role):
        for tag in tags:
            if tag['key'] == 'badges':
                badges = tag['value'].split(',')
                for badge in badges:
                    if badge.strip() == role:
                        return True
        return False

    if message.startswith('!hello'):
        # Respond with a greeting
        if username not in names:
            names.append(username)
            response = f'Hello, {username}!'
        else:
            response = f"Didn't we already greet each other, {username}?"
        send_message(response)
    elif message.startswith('!commands'):
        # Respond with a list of commands
        send_message('Available commands: !hello, !herald [message], !dadjoke, !lore, !roll6, !roll20, !dcount, !lurk')
    elif message.startswith('!dadjoke'):
        # Respond with a dad joke
        dadjoke = Dadjoke()
        for line in dadjoke.joke.splitlines():
            send_message(line)
    elif message.startswith('!roll6'):
        #Respond with a random number between 1 and 6
        send_message("The die came up "+str(random.randint(1, 6))+"!")
    elif message.startswith('!roll20'):
        #Respond with a random number between 1 and 20
        send_message("The die came up "+str(random.randint(1, 20))+"!")
    elif message.startswith('!lurk'):
        # Respond with a message acknowledging a lurker
        response = f"Lurking, are we {username}? Very well, I'll keep the flame lit for you!"
        send_message(response)
    elif message.startswith('!lore'):
        # Respond with a piece of random lore
        response = random.choice(lore)
        send_message(response)
    elif message.startswith('!herald') and Openai_client is not None:
         # Generate a response using ChatGPT
        message = re.sub("!herald\s?", "", message) 
        response = generate_response(message).splitlines()
        for line in response:
            send_message(line)
    elif message.startswith("!setdeath"):
        if has_role('broadcaster/1') or has_role('moderator/1'):
        # Manually set the death counter by extracting a number from the message sent by the broadcaster or a mod
            pattern = r'\d+'
            match = re.search(pattern, message)
            if match:
                number = match.group()
                counter = int(number)
                send_message(f"Understood. Death counter set to {counter}.")
            else:
                send_message(f"I didn't understand that. Can you try again?")
    elif message.startswith('!death'):
        if has_role('broadcaster/1') or has_role('moderator/1'):
            # Respond with a message acknowledging a death and increase death counter by 1, if sent by the broadcaster or a mod
            counter = counter + 1
            response = f"{channel} has been slain! Total Deaths: {counter}"
            send_message(response)
    elif message.startswith('!dcount'):
        # Respond with the current death counter
        if counter == 0:
            response = f"So far, {channel} hasn't died that I know of. Are we supposed to be keeping track of that? No one reported any deaths to me."
        if counter == 1:
            response = f"So far, {channel} has died once."
        else:
            response = f"So far, {channel} has died {counter} times."
        send_message(response)


def timed_message():
    global message_count
    while True:
        #Posts an invitation to join Discord every 10 minutes, but only if at least 5 other messages have been posted in chat since the last time this was posted
        if message_count > 5:
            message_count = 0
            #send_message("Come to the Forever Rolling discord server, and join in our Jolly Cooperation! https://discord.gg/AjqUSfcd3r")
            send_message("Wil and his wife Ariarosso are raising money to help a local, no-kill animal shelter. If goals are met, they'll eat Beanboozle Spicy Jelly Beans! Click here for info and to donate: https://www.paypal.com/pools/c/93QqD0wxIv")
        time.sleep(600)


def generate_response(message):
    # Generate a response using ChatGPT
    response = Openai_client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        n = 1,
        messages=[
        { 
          "role": "system", 
          # Use this to help fine-tune the responses you receieve. You can establish the personality of the bot, any self-identifying info you want it to have, and message format.
          "content": "You are the Sapphire Herald, a calm, friendly woman who is the assistant of Lorekeeper Wilveren. Specifically, you are a Fire Keeper as they are portrayed in the Dark Souls games. Please summarize to keep responses brief, and avoid using newlines."
        },
        {
            "role": "user",
            "content": message
        },
    ],
        timeout= 30,
        max_tokens = 100
    )

    return response.choices[0].message.content

# Connect to the Twitch IRC server and request the needed capabilities to recognize a user's roles
client = irc.client.Reactor()
client.add_global_handler('welcome', on_welcome)
client.add_global_handler('pubmsg', on_pubmsg)
c = client.server().connect(server, port, nickname, password=f'oauth:{token}')
c.cap('REQ', ':twitch.tv/tags')

# Start the periodic message thread which will ensure timed messages are posted to the chat
thread = threading.Thread(target=timed_message)
thread.daemon = True
thread.start()

# Start the main event loop
client.process_forever()
