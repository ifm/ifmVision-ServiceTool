from datetime import timedelta
from timeit import default_timer as timer
import time
import os


class LoggerBoxer(object):
    def __init__(self, listWidget):
        self.listWidget = listWidget

        self.total_bar_steps = None
        self.timer_start = None

    def add_log_entry(self, msg, cnt=-1.0):
        if cnt > 1:
            last_item_index = self.listWidget.count()
            self.listWidget.takeItem(last_item_index - 1)

        self.listWidget.addItem(str(msg))
        if cnt >= 1:
            _time_elapsed = str(timedelta(seconds=timer() - self.timer_start))
            _bar = self.progress_bar(count=cnt, total=self.total_bar_steps, suffix=_time_elapsed)
            self.listWidget.addItem(_bar)
        time.sleep(0.2)
        self.listWidget.scrollToBottom()
        time.sleep(0.2)

    def clear_all_entries(self):
        self.listWidget.clear()

    @staticmethod
    def progress_bar(count, total, suffix=''):
        """Returns a progress bar as string."""
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '#' * filled_len + ' ' * (bar_len - filled_len)
        if suffix:
            return '[%s] %s%s ... %s\r' % (bar, percents, '%', suffix)
        return '[%s] %s%s' % (bar, percents, '%')

    def check_or_make_log_file_path(self, path):
        dir_path = os.path.dirname(os.path.realpath(path))
        if not os.path.exists(dir_path):
            # directory does not exist
            os.makedirs(dir_path)
            self.add_log_entry(msg="Log file path missing. Created path: " + str(dir_path))

    def save_log(self, log_file_path):
        self.check_or_make_log_file_path(path=log_file_path)
        self.add_log_entry(msg="Writing log to log file: " + str(log_file_path))
        itemsTextList = [str(self.listWidget.item(i).text()) for i in range(self.listWidget.count())]

        with open(log_file_path, "w") as f:
            f.writelines([f"{line}\n" for line in itemsTextList])
        f.close()
