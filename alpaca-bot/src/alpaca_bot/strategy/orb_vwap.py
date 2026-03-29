from datetime import time
from alpaca_bot.model import Bar, Order, BracketOrder, StopLossUpdate

class ORBVwap:
    def __init__(self, symbol, orb_end = time(9, 45), reward_ratio = 10):
        self.symbol = symbol
        self.reward_ratio = reward_ratio
        self.orb_start = time(9, 30)
        self.orb_end = orb_end
        self.orb_high = 0.0
        self.orb_low = float('inf')
        self.orb_range = 0
        self.currently_trading = False
        self.has_traded_today = False
        self.stop_loss = 0

    def process_bar(self, bar: Bar) -> Order | None:
        curr_time = bar.timestamp.time()

        if self.orb_start <= curr_time <= self.orb_end:
            self.orb_high = max(self.orb_high, bar.high)
            self.orb_low = min(self.orb_low, bar.low)
            return None

        if curr_time >= self.orb_end and (self.orb_low == float("inf") or self.orb_high == 0):
            return None

        if self.orb_range == 0:
            self.orb_range = self.orb_high - self.orb_low

        if not self.has_traded_today:
            if self._found_entry(bar):
                self.stop_loss = self.orb_low
                self.has_traded_today = True
                self.currently_trading = True
                order = BracketOrder(
                    symbol = self.symbol,
                    price = bar.close,
                    shares = 0,
                    stop_loss = self.stop_loss,
                    take_profit = self.orb_high + self.orb_range * self.reward_ratio
                )
                return order
        elif self.currently_trading:
            new_stop_loss = self._update_stop_loss(bar)
            if new_stop_loss is not None:
                self.stop_loss = new_stop_loss
                return StopLossUpdate(self.symbol, self.stop_loss)

        return None

    def _found_entry(self, bar) -> bool:
        if bar.vwap is None:
            return False
        if bar.close > self.orb_high and bar.close > bar.vwap:
            return True
        return False

    def _update_stop_loss(self, bar) -> float | None:
        if bar.high >= self.stop_loss + self.orb_range / 4:
            return self.stop_loss + self.orb_range / 4
        return None

