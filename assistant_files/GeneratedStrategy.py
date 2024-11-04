from LoggedStrategy import *
import backtrader as bt 

class GeneratedStrategy(LoggedStrategy):
    params = (
        ('tenkan_period', 9),
        ('kijun_period', 26),
        ('s_span_a_period', 26),
        ('s_span_b_period', 52),
    )

    def __init__(self):
        self.tenkan = bt.indicators.Ichimoku(self.data, 
                                             tenkan=self.params.tenkan_period,
                                             kijun=self.params.kijun_period)
        self.kijun = self.tenkan.kijun
        self.cloud_a = self.tenkan.senkou_a
        self.cloud_b = self.tenkan.senkou_b

    def next(self):
        if not self.position:  # Not in a position
            if self.data.close[0] > self.cloud_a[0] and self.data.close[0] > self.cloud_b[0]:
                # Buy signal
                self.buy()
        else:  # In a position
            if self.data.close[0] < self.cloud_a[0] or self.data.close[0] < self.cloud_b[0]:
                # Sell signal
                self.sell()

    @staticmethod
    def get_optimisation_range():
        return {
            'tenkan_period': range(5, 20, 1),
            'kijun_period': range(15, 40, 1),
            's_span_a_period': range(20, 30, 1),
            's_span_b_period': range(40, 60, 1),
        }