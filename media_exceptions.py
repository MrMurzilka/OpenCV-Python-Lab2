#Общий класс исключений
class MediaError(Exception):
    def __init__(self, message, file_path=None):
        self.file_path = file_path
        super().__init__(message)

#Исключение для ошибок загрузки файла
class FileLoadError(MediaError):
    def __init__(self, file_path, reason="Failed to load video"):
        self.message = f"{reason}: {file_path}"
        super().__init__(self.message, file_path)

#Исключение для некорректных данных в файле
class InvalidDataError(MediaError):
    def __init__(self, file_path, data_type="Video"):
        self.message = f"Corrupted data in the file {file_path} ({data_type})"
        super().__init__(self.message, file_path)

#Исключение для ошибок декодирования видео
class VideoDecodeError(MediaError):
    def __init__(self, file_path, reason = "Failed to decode video"):
        self.message = f"{reason}: {file_path}"        
        super().__init__(self.message, file_path)

#Исключение для неподдерживаемых кодеков
class UnsupportedCodecError(MediaError):
    def __init__(self, file_path, codec):
        self.message = f"{codec} is unsupported: {file_path}"
        super().__init__(self.message, file_path)

#Скрипт для проверки работы исключений
if __name__ == "__main__":
    try:
        raise FileLoadError("","")
    except MediaError as e:
        print(f"{e}")