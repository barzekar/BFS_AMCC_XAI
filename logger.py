class Logger:
    queue = []

    def log_info(self, text):
        print(text)
        Logger.queue.append(text)

    def collect(self):
        result = Logger.queue.copy()
        Logger.queue.clear()
        return result
