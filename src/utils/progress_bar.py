"""Creates a progress bar
"""

from proglog import TqdmProgressBarLogger

class VideoProgressBar(TqdmProgressBarLogger):
    def callback(self, **changes):
        # Every time the logger is updated, this function is called
        if len(self.bars):
            percentage = next(reversed(self.bars.items()))[1]['index'] / next(reversed(self.bars.items()))[1]['total']