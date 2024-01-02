


import datetime


class Logger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None

    def open_log(self):
        self.file = open(self.file_path, 'a')  # 'a' mode appends to the file, creates if not exists
        current_time = datetime.datetime.now()
        # 将时间转换为字符串形式
        time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.writeline("\n New logging start at\t"+time_string)


    def writeline(self, message):
        log_line = f"{message}\n"
        self.file.write(log_line)

    def close_log(self):
        current_time = datetime.datetime.now()
        # 将时间转换为字符串形式
        time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.writeline("Logging end at\t"+time_string+'\n')
        self.file.close()