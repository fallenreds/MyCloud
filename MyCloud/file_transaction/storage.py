import telebot
from .mixins import SendFileMixin, GetFileMixin


class TelegramStorage:
    def __init__(self, token='5543008601:AAGIRHOKP4BNJwPgGMLFziKdGbtqWBsgQEo'):
        self.token = token
        self.storage_id = 516842877
        self.bot = telebot.TeleBot(token)


class UploadFile(SendFileMixin):
    def upload_file(self, file):
        instance = TelegramStorage()
        return self.upload(file, instance=instance)


class DownloadFile(GetFileMixin):
    def download_file(self, data):
        instance = TelegramStorage()
        return self.download(data, instance)
