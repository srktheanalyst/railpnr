import telebot
import requests

# Initialize the Telegram bot (replace 'your_telegram_bot_token' with your actual bot token)
bot = telebot.TeleBot("6803862348:AAEpObDx5rEF09Z82CYN9zxTdcJKvwt4-3k")

# RapidAPI Headers
headers = {
    "X-RapidAPI-Key": "a2b4fba7b9msha9834eae6737f34p1207b7jsn579803c69acb",
    "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    # Handle the start command
    bot.reply_to(message, "Welcome to the PNR status bot! Please enter your 10-digit PNR number.")

@bot.message_handler(func=lambda message: True)
def handle_pnr(message):
    # Handle the PNR number entered by the user
    pnr_number = message.text.strip()
    pnr_status = get_pnr_status(pnr_number)
    bot.reply_to(message, pnr_status)

def get_pnr_status(pnr_number):
    url = "https://irctc1.p.rapidapi.com/api/v3/getPNRStatus"
    querystring = {"pnrNumber": pnr_number}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        pnr_status = response.json()
    except requests.exceptions.HTTPError as err:
        pnr_status = f"HTTP Error: {err}"
    except requests.exceptions.RequestException as err:
        pnr_status = f"Request Error: {err}"
    except Exception as err:
        pnr_status = f"An error occurred: {err}"
    
    return str(pnr_status)  # Convert the response to a string for Telegram

# Start the bot
bot.polling()
