import json
import time

class BaseSocket:

    def __init__(self):
        self.market = None

    # do all of the saves & broadcasts here
    def on_message(self, message):
        print(message)
        # maybe log original message?
        parsed_message = self.market_parse_message(message)


    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def stop_ws(self):
        self.market_close_ws()

    def start_ws(self):
        self.market_start_ws()


    # Methods below are implemented by exchanges. Used to
    def market_start_ws(self):
        raise NotImplementedError("market_start_ws must be implemented by an exchange")

    def market_close_ws(self):
        raise NotImplmentedError("market_close_ws must be implemented by an exchange")

    def market_init(self):
        raise NotImplementedError("market_init must be implemented by an exchange")

    def market_parse_message(self, message):
        raise NotImplementedError("market_parse_message must be implemented by an exchange")
