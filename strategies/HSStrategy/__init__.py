from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import pandas as pd


class MovingAverageStrategy(Strategy):
    """
    Moving Average Strategy
    A strategy that enters long position if the fast moving average (50-period) crosses above the slow moving average (200-period)
    and enters short position if the fast moving average crosses below the slow moving average.
    A stop loss limit of 1% is applied by default. If the total capital is greater than 5% of the initial capital ($1000),
    the stop loss limit increases to 1.15%. If the total capital is greater than 7% of the initial capital ($1000),
    the stop loss limit increases to 1.25%. The strategy avoids operating during NFP (Non-Farm Payrolls) days.
    """

    def __init__(self):
        super().__init__()
        self.vars["slow_ma_period"] = 200
        self.vars["fast_ma_period"] = 50
        self.vars["stop_loss_limit"] = 0.01
        self.vars["NFP_days"] = [pd.to_datetime(
            "first friday of the month") + pd.DateOffset(months=i) for i in range(12)]

    @property
    def slow_ma(self):
        return ta.sma(self.candles, self.vars["slow_ma_period"])

    @property
    def fast_ma(self):
        return ta.sma(self.candles, self.vars["fast_ma_period"])

    def should_long(self) -> bool:
        return self.price > self.slow_ma and self.fast_ma > self.slow_ma and self.date not in self.vars["NFP_days"]

    def should_short(self) -> bool:
        return self.price < self.slow_ma and self.fast_ma < self.slow_ma and self.date not in self.vars["NFP_days"]

    def should_cancel(self) -> bool:
        return False

    def go_long(self):
        if self.total_capital > 1000 * 1.05:
            self.vars["stop_loss_limit"] = 0.0115
        if self.total_capital > 1000 * 1.07:
            self.vars["stop_loss_limit"] = 0.0125
        qty = utils.size_to_qty(
            self.capital, self.price, fee_rate=self.fee_rate)
        stop_loss_price = self.price * (1 - self.vars["stop_loss_limit"])
        self.buy = qty, self.price, stop_loss_price

    def go_short(self):
        qty = utils.size_to_qty(
            self.capital, self.price, fee_rate=self.fee_rate)
        stop_loss_price = self.price * (1 + self.vars["stop_loss_limit"])
        self.sell = qty, self.price, stop_loss_price

    def update(self):
        pass
