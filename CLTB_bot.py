import sys

from notifiers import get_notifier
import requests
import time
import configparser


class ConfigError(Exception):
    pass


class Scanner:
    """
    Class to scan new symbol listings on Binance and send notifications.
    """

    def __init__(self, endpoint=None):
        """
        Initialize a Scanner instance.

        :param endpoint: Optional, the API endpoint to use for symbol information.
                         Valid options are '-futuresInfo' and '-exchangeInfo'.
        """
        self.endpoint = endpoint
        # Read the config file and check that required values are present
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.TOKEN = self.config['telegram']['telegram_token']
        self.USER_ID = self.config['telegram']['user_id']

    def set_config(self):
        """
        Set new Telegram credentials in the config file if the token and id are not specified in the file.
        """
        self.config['telegram'] = {}
        print("Telegram bot token you can get here --> https://t.me/BotFather")
        self.config['telegram']['telegram_token'] = input("Enter your Telegram bot token: ")
        print("Telegram user ID you can get here --> https://t.me/getmyid_bot")
        self.config['telegram']['user_id'] = input("Enter your Telegram user ID: ")
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def config_check(self):
        """
        Checking that Telegram credentials are present in the config file and raise an error in case of missing data.
        """
        if not (self.TOKEN and self.USER_ID):
            raise ConfigError

    def endpoint_assignment(self):
        """
        Assign an API endpoint based on a user-specified endpoint setting.
        :return: The API endpoint URL.
        :raises ValueError: If no endpoint parameter was given.
        """
        if not self.endpoint:
            raise ValueError

        if self.endpoint == '-futuresInfo':
            return 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        if self.endpoint == '-exchangeInfo':
            return 'https://api.binance.com/api/v1/exchangeInfo'

    def get_binance_symbols(self):
        """
        Retrieving a list of all symbols on Binance.
        :return: A list of symbols.
        """

        # API endpoint to get a list of all symbols
        designated_endpoint = self.endpoint_assignment()

        # Make a GET request to the endpoint
        response = requests.get(designated_endpoint)
        # Check the status code of the response
        if response.status_code == 200:
            # Return the list of symbols
            data = response.json()
            return [symbol["symbol"] for symbol in data["symbols"]]
        else:
            # Return None if the status code is not 200
            return None

    def sending_notifications(self, message):
        """
        Send a notification to the user via Telegram.
        :param message: The message to send.
        :return: The response from Telegram.
        """
        telegram = get_notifier('telegram')
        return telegram.notify(token=self.TOKEN, chat_id=self.USER_ID, message=message)

    def start(self):
        """
        Continuously check for new symbol listings on Binance and send notifications when found.
        """
        # Get the current list of symbols
        symbols = self.get_binance_symbols()
        if symbols is None:
            return

        print('###################################################################\n'
              '### The program has SUCCESSFULLY STARTED its work, ################\n'
              '### you will receive a notification in the specified telegram #####\n'
              '### bot for the specified user when new tokens are listed #########\n'
              '###################################################################\n')
        # Continuously check for new listings
        while True:
            new_symbols = self.get_binance_symbols()
            if new_symbols:
                # Compare the new list of symbols to the current list
                new_listings = set(new_symbols) - set(symbols)
                # Notify for each new listing
                for symbol in new_listings:
                    endpoint_text = ' Futures.' if self.endpoint == '-futuresInfo' else '.'
                    notification = f"{symbol} is now listed on Binance{endpoint_text}"
                    self.sending_notifications(notification)
                # Update the current list of symbols
                symbols = new_symbols
            time.sleep(30)


# Usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        endpoint = sys.argv[1]
        scan = Scanner(endpoint=endpoint)
    else:
        # You can add options 'scan = Scanner(endpoint="-futuresInfo" or "-exchangeInfo") to permanently use the program
        # with these parameters instead of exiting the program from the console'
        scan = Scanner()
    try:
        scan.config_check()
        scan.start()
    except ValueError as e:
        print('Please choose one of the options:\n'
              '"-futuresInfo" or "-exchangeInfo".\n'
              'Example: "python3 scanner.py -futuresInfo".')
    except ConfigError as e:
        scan.set_config()
        scan.start()
