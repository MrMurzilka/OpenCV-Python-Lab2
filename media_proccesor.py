from abc import ABC, abstractmethod
from pathlib import Path
from media_exceptions import (
    MediaError,
    FileLoadError,
    InvalidDataError,
    UnsupportedCodecError,
    )

class MediaProcessor(ABC):
    '''Abstract base class for media processing.'''

    @abstractmethod
    def process(self, file_path):
        pass

    @abstractmethod
    def validate(self, file_path):
        pass

class VideoProcessor(MediaProcessor):
    '''Class for processing video files.'''

    SUPPORTED_EXTENSIONS = {".mp4", ".mkv"}

    #Extracting video metadata
    def get_video_info(self, file_path):
        cap = self.load_video(file_path)

        try:
            import cv2
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            #Processing errors with invalid metadata
            if fps is None or fps < 0:
                raise InvalidDataError(str(file_path))
            
            if width is None or width < 0:
                raise InvalidDataError(str(file_path))
            
            if height is None or height < 0:
                raise InvalidDataError(str(file_path))
                        
            return{
                "file_path": str(file_path),
                "fps": fps,
                "frame_count": frame_count,
                "width": width,
                "height": height
                }

        #Releasing OpenCV resources
        finally:
            cap.release()

    #Method for loading video with checking on exceptions
    def load_video(self, file_path):
        #Extracting file path
        path = Path(file_path)

        #Checking if path leads to existing file(and if it's file)
        if not path.is_file():
            raise FileLoadError(str(path), "No such file")
        #Checking if file extension is in SUPPORTED_EXTENSIONS
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedCodecError(str(path), path.suffix or "undefined")

        #Trying to import OpenCV module
        try:
            import cv2
        except ImportError as e:
            raise MediaError(str(path)) from e

        #Opening the video
        cap = cv2.VideoCapture(str(path))

        #If there are errors while opening release the OpenCV 
        #resources and raised an custom exception
        if not cap.isOpened():
            cap.release()
            raise FileLoadError(str(path))

        #If there are no errors and exceptions return the
        #VideoCapture object
        return cap

    #Method for processing video objects
    #The logic can be extended in term of `processing`
    #e.g. with Filters from Lab1
    def process(self, file_path):
        #Extracting video metadata
        info = self.get_video_info(file_path)

        #Here also we can get VideoCapture object and do processing stuff
        
        print(f"""{file_path}: {info['width']} x {info['height']}""")

    #Validating if file with proposed path is exists and have 
    #supported extension
    def validate(self, file_path):
        path = Path(file_path)

        if not path.is_file() or path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return False

        try:
            import cv2
        except ImportError:
            return False

        cap = cv2.VideoCapture(str(path))
        try:
            return cap.isOpened()
        finally:
            cap.release()

#Test script
if __name__ == "__main__":
    processor = VideoProcessor()

    if processor.validate("..\\Lab1\\source\\test_video1.mp4"):
        processor.process("..\\Lab1\\source\\test_video1.mp4")