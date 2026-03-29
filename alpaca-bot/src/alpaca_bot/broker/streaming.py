from alpaca.data.live import StockDataStream
from alpaca.data.models.bars import Bar as AlpacaBar
from alpaca_bot.config import STOCKS

class StreamingClient:
    def __init__(self, api_key, api_secret):
        self.client = StockDataStream(api_key, api_secret)

    def stream(self):
        for stock in STOCKS:
            self.client.subscribe_bars(self._process_bar, stock)
        self.client.run()

    async def _process_bar(self, alpaca_bar: AlpacaBar) -> None:
        pass


