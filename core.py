import time
import sys

class CryptoGuardian:
    def __init__(self, limits):
        self.limits = limits
        self.stream = iter(sys.stdin.readline, '')

    def sanitize(self, raw_input):
        try:
            val = float(raw_input.strip())
            if self.limits['min'] <= val <= self.limits['max']:
                return val
        except ValueError:
            pass
        return None

    def run_process(self):
        print('Awaiting valid trade volume...')
        for line in self.stream:
            trade = self.sanitize(line)
            if trade:
                self.execute(trade)
            else:
                print(f'Ignored: {line.strip()} is invalid/out-of-bounds')

    def execute(self, amount):
        # Simulation of core crypto logic
        print(f'Processing {amount:.4f} units')

if __name__ == '__main__':
    bounds = {'min': 0.001, 'max': 100.0}
    bot = CryptoGuardian(bounds)
    bot.run_process()