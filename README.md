# Checking Listing Tokens Binance

The idea is to notify the user about the new listing of tokens on the Binance exchange. Information about the new listing will be sent to the telegram bot and the message will be seen only by the user whose id is specified in the config file.

Installation.
  It is advisable to put the bot in a server where it will work permanently
  Istruction:
    1) git clone https://github.com/GreenFor3st/CLTB_bot.git
    2) cd <path.../CLTB_bot>
    3) pip3 install -r requirements.txt
    4) python3 CLTB_bot.py -futuresInfo (or '-exchangeInfo')
    5) wait for the message 

Technologies and dependencies.
  The technology of the program is arranged as follows:
  Send a request to the Binance endpoint every 30 seconds subtracting the data (converted to a set object) of the previous request from the data of the new   one. Thus, if the difference is not equal to 0, that is, False, then the user will be notified.

  The program uses the notifiers library to send messages to telegrams by user ID and configparser to work with .ini files.
  
 List of authors.
  Ivan Peshekhonov.
