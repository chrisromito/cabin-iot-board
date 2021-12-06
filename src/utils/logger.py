from settings import DEBUG


class Logger:
    def __init__(self, max_logs=3, max_errors=1):
        self.logs = []
        self.max_logs = max_logs
        self.errors = []
        self.max_errors = max_errors

    def log(self, line):
        try:
            self.logs.append(line)
            if len(self.logs) > self.max_logs:
                self.write_logs()
            return self
        except Exception as err:
            print('Caught an error whilst trying to log...')
            print(err)
            print('Original log:')
            print(line)

    def error(self, err):
        self.debug(err)
        try:
            self.errors.append(err)
            if len(self.errors) > self.max_errors:
                self.write_errors()
        except Exception as fuck:
            print('Caught an error while trying to log an error...')
            print(fuck)

    def write_logs(self, file_path='logs.txt'):
        text_to_write = '\n'.join(
            list(map(str, self.logs))
        )
        with open(file_path, 'a') as logs:
            logs.write(text_to_write)
        self.logs = []

    def write_errors(self):
        text_to_write = '\n'.join(
            list(map(str, self.errors))
        )
        with open('/error_logs.txt', 'a') as logs:
            logs.write(text_to_write)
        self.errors = []

    def debug(self, message):
        if DEBUG:
            print(message)


log = Logger()
