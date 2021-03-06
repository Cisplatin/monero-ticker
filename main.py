from collections import OrderedDict

import rumps
from json import loads
from urllib2 import build_opener

class MoneroTicker(rumps.App):
    ICON = "monero.ico"
    UPDATE_FREQUENCY = 60
    MONERO_URL = "http://moneropric.es/fiat.json"
    DEFAULT_CURRENCY = "USD"
    SYMBOLS = OrderedDict([
        ("USD" , "$"),
        ("CAD", "$"),
        ("EUR" , u"\u20AC"),
        ("GBP", u"\u00A3"),
        ("BTC", u"\u0180"),
    ])

    def __init__(self):
        super(MoneroTicker, self).__init__(type(self).__name__, icon=MoneroTicker.ICON)
        self.currency = MoneroTicker.DEFAULT_CURRENCY
        self.padded = False
        self.run()

    @rumps.clicked("About")
    def about(self, _):
        # TODO What do people put on about pages?
        text = \
        """
        Feel free to donate to MoneroTicker!
        <address_redacted>
        """
        window = rumps.Window(title="Monero Ticker", message=text, ok=None, dimensions=(0,0))
        window.icon = MoneroTicker.ICON
        window.run()

    @rumps.clicked("Preferences")
    def preferences(self, _):
        text = \
        """
        Select the currency you would like to display the price in.
        """
        window = rumps.Window(title="Preferences", message=text, ok="Cancel", dimensions=(0,0))
        window.icon = MoneroTicker.ICON
        window.add_buttons(MoneroTicker.SYMBOLS.keys())
        response = window.run().clicked

        # The response will be one if the user pressed cancel, else will be 2, 3, ...
        if response > 1:
            self.currency = MoneroTicker.SYMBOLS.keys()[response - 2]
            self.update_price('_')

    @rumps.timer(UPDATE_FREQUENCY)
    def update_price(self, sender):
        # To get around CloudFlare, we set the User-Agent of our opener
        opener = build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        response = opener.open(MoneroTicker.MONERO_URL).read()

        # Get the currency we're interested in and set the ticker title
        entry = filter(lambda x: x["code"] == self.currency, loads(response))[0]["fiat-rate"]
        title = MoneroTicker.SYMBOLS[self.currency] + str(format(entry, "0.2f"))

        # TODO: We manually pad the price the first time the ticker is loaded because of a
        #       glitch in rumps. It looks a bit weird when it changes to the first non-padded
        #       version. Need some sort of fix so that it stops doing that.
        if not self.padded:
            title += " " * 5
            self.padded = True
        self.title = title

if __name__ == "__main__":
    MoneroTicker()
