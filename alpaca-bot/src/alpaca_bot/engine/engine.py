from alpaca_bot.broker import StreamingClient, TradingClient
from alpaca_bot.config import STOCKS, max_trade_amount
from alpaca_bot.strategy import ORBVwap
from alpaca.data.models import Bar as AlpacaBar

class AlpacaEngine:
    def __init__(self, streaming_client: StreamingClient, trading_client: TradingClient):
        self.streaming_client = streaming_client
        self.trading_client = trading_client
        self.strategies: dict[str, ORBVwap] = {
            s: ORBVwap(symbol = s)
            for s in STOCKS
        }
        self.max_trade_amt = max_trade_amount

    def stream_bars(self):
        self.streaming_client.stream()


    async def _process_bar(self, alpaca_bar: AlpacaBar):

        pass

    def _handle_buy(self):
        pass

    def _handle_stop_loss_update(self):
        pass