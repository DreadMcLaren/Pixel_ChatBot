# Installation Instructions

**NOTE:** This install guide was created using linux Ubunutu and assumes you've already gathered your telegram token and openai api key.

1. SSH into server
```
ssh USERNAME@IP-ADDRESS
```

2. Update the server
```
sudo apt-get update && sudo apt-get upgrade -y
```

3. Install Python, Pip, Git and Screen
```
sudo apt-get install python3 python3-pip screen git -y
```

4. Install bot dependencies
```
pip3 install python-telegram-bot==13.7 openai python-dotenv cryptography
```

5. Clone the repository
```
git clone https://github.com/DreadMcLaren/Pixel_Chatbot.git
```

6. Navigate to where you saved it
```
cd path/to/bot
```

7. Open the ```.env``` file and edit the required information
```
nano .env
```

Add your Telegram token, OpenAI API key and desired password and save it ```CTRL + X``` and ```Y``` keeping the same file name
```
TELEGRAM_API_TOKEN=Your_Telegram_API_Token
OPENAI_API_KEY=Your_OpenAI_API_Key
LOG_FILE_PASSWORD=Your_Password
```

8. Start the bot

```
python3 bot.py
```

**The bot will now be running and listening for messages on Telegram. The log file (```Pixelchatbot.log```) will be placed in the same directory your bot is in.**

To generate an image with DALL·E AI using Telegram, use ```/image``` followed by your prompt.

Example:

```
/image a white siamese cat
```

--------------------------------------------
**OPTIONAL:**

If you want to run the bot detached from the main console window, use Screen.

```
cd path/to/bot
```

```
screen -S bot-session
```

```
python3 bot.py
```

To detatch from the running bot, press ```Ctrl + A``` followed by ```D```
