try:
    import urequests as requests
except ImportError:
    import requests
from constants import API_URL


def log(data, endpoint=''):
    try:
        path = endpoint.replace('//', '/')
        url = ''.join([API_URL, path])
        req = requests.post(url, json=data)
        req.close()
    except Exception as error:
        log_error(error)


def flight_complete():
    url = ''.join([API_URL, '/flight/complete'])
    try:
        req = requests.post(url, json={})
        req.close()
    except:
        pass


def log_error(err):
    try:
        with open('error.txt', 'a') as f:
            f.write(err)
            f.close()
    except:
        pass
    try:
        url = ''.join([API_URL, '/error'])
        req = requests.post(url, json={
            'error': str(err)
        })
        req.close()
    except:
        pass


class Logger:
    def __init__(self, max_logs=3, max_errors=1):
        self.logs = []
        self.max_logs = max_logs
        self.errors = []
        self.max_errors = max_errors

    def log(self, line):
        self.logs.append(line)
        if len(self.logs) > self.max_logs:
            self.write_logs()
            self.logs = []
        return self

    def error(self, err):
        try:
            self.errors.append(err)
            if len(self.errors) > self.max_errors:
                self.write_errors()
                self.errors = []
        except Exception as fuck:
            print('Caught an error while trying to log an error...')
            print(fuck)

    def write_logs(self, file_path='logs.txt'):
        with open(file_path, 'a') as logs:
            logs.writelines(self.logs)

    def write_errors(self):
        with open('error_logs.txt', 'a') as logs:
            logs.writelines(self.errors)
