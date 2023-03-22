from notifiers import get_notifier

import requests
import time

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# add user ID's and telegram token
TOKEN = config['telegram']['telegram_token']
USER_ID = config['telegram']['user_id']


def get_binance_symbols():
    # API endpoint to get a list of all symbols
    endpoint = "https://api.binance.com/api/v1/exchangeInfo"

    # Make a GET request to the endpoint
    response = requests.get(endpoint)
    # Check the status code of the response
    if response.status_code == 200:
        # Return the list of symbols
        data = response.json()
        return [symbol["symbol"] for symbol in data["symbols"]]
    else:
        # Return None if the status code is not 200
        return None


def notification_telegram_bot(message: str):
    telegram = get_notifier('telegram')

    return telegram.notify(token=TOKEN, chat_id=USER_ID, message=message)


def notify_new_listing():
    # Get the current list of symbols
    symbols = get_binance_symbols()
    if symbols is None:
        return

    # Continuously check for new listings
    while True:
        new_symbols = get_binance_symbols()
        print(new_symbols)
        if new_symbols:
            # Compare the new list of symbols to the current list
            new_listings = set(new_symbols) - set(symbols)
            print(new_listings)

            # Notify for each new listing
            for symbol in new_listings:
                notification = f"{symbol} is now listed on Binance!"
                notification_telegram_bot(notification)
            # Update the current list of symbols
            symbols = new_symbols
        time.sleep(1)


# Example usage
notify_new_listing()
