import requests
from telegram import * 
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

def get_Download_URL_From_API(url):
    API_URL = "https://genius.p.rapidapi.com/artists/16775/songs"
    querystring = {"url": f"{url}"}

    headers = {
        "X-RapidAPI-Host": "genius.p.rapidapi.com",
	    "X-RapidAPI-Key": "2e6fdb04f5mshb91addcae7e3ff8p1f68aejsn4b385546c261" # This is your API key token. Keep it secret!
    }

    response = requests.request("GET", API_URL, headers=headers, params=querystring)
    data = response.json()
    return data['streams'][0]['url']

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to URL downloader !\nPlease provide a valid url')

def textHandler(update: Update, context: CallbackContext) -> None:
    if update.message.parse_entities(types=MessageEntity.URL):
        update.message.reply_text(text='You sent a valid URL!', quote=True)

def main():
    TOKEN = "YOUR BOT TOKEN"
    
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, textHandler, run_async=True))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()