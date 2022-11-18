import io


class SendFileMixin:
    def __init__(self):
        self.chunk_size = 1024 * 1000  # Bytes, 100kb
        self.chunk = 0
        self.array_of_chunks = []

    def upload(self, file, instance):
        return self._split_file(file, instance)

    def _split_file(self, file, instance):
        file_name = file.name
        byte = file.read(self.chunk_size)

        while byte:
            chunk_name = self.__get_chunk_name(file_name)
            file_id = self.send_file(file=byte, file_name=chunk_name, instance=instance)
            self.chunk += 1
            byte = file.read(self.chunk_size)
            self.array_of_chunks.append(str(file_id))
        return self.__list_to_str()

    @staticmethod
    def send_file(file, file_name, instance):
        message = instance.bot.send_document(instance.storage_id, file, visible_file_name=file_name)
        return message.message_id

    def __get_chunk_name(self, file_name):
        header = file_name.split('.')[:-1]
        return f'{header}_chunk_{self.chunk}.txt'

    def __list_to_str(self):
        return " ".join(self.array_of_chunks)


class GetFileMixin:
    def __init__(self):
        self.current_file = b''

    def download(self, data, instance):
        return self._merge_f(data, instance)

    @staticmethod
    def __str_to_list(message):
        return message.split()

    @staticmethod
    def refresh_id(file_data, instance):
        chat_id = instance.storage_id
        from_chat_id = instance.storage_id
        message_id = file_data
        fresh_message = instance.bot.forward_message(chat_id, from_chat_id, message_id)
        return fresh_message.document.file_id

    @staticmethod
    def get_file(instance, file_id):
        file = instance.bot.get_file(file_id)
        return io.BytesIO(instance.bot.download_file(file.file_path))

    def _merge_f(self, data, instance):
        id_messages = self.__str_to_list(message=data['messages'])

        for file_data in id_messages:
            file_id = self.refresh_id(file_data, instance)
            file = self.get_file(instance, file_id)
            self.current_file += file.read()
        print('Я закончил сойденение')
        return io.BytesIO(self.current_file)
