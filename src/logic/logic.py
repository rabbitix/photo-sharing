import logging

from fastapi import UploadFile
from telegram import Bot

from src.repository.foto_repository import FotoRepository


class FotoLogic:
    def __init__(self):
        self.repository = FotoRepository()

    async def get_queue_worker(self):
        await self.repository.get_queue_worker()

    def _get_bot(self, token: str) -> Bot:
        return Bot(token=token)

    async def send_photo(self, token: str, chat_id: str, file: UploadFile) -> None:
        bot = self._get_bot(token)
        file_name = file.filename
        raw_file = await file.read()
        pm = None
        if file.size < 10 * 1024 * 1024:  # 10mb
            pm = await bot.send_photo(chat_id=chat_id, photo=raw_file)
            logging.info("sent photo to %s", chat_id)

            await bot.send_document(
                chat_id=chat_id,
                document=raw_file,
                filename=file_name,
                reply_to_message_id=pm.message_id if pm else None,
            )
            logging.info("sent document to %s", chat_id)
        else:
            """from PIL import Image
            import io

            def resize_image_bytes(image_bytes, max_size_mb=10):
                # Open the image from bytes
                img = Image.open(io.BytesIO(image_bytes))

                # Get the original format
                img_format = img.format

                # Initial quality
                quality = 95

                while True:
                    # Save the image to a bytes buffer
                    buffer = io.BytesIO()
                    img.save(buffer, format=img_format, quality=quality)

                    # Get the size of the image in bytes
                    size_mb = len(buffer.getvalue()) / (1024 * 1024)

                    if size_mb <= max_size_mb:
                        return buffer.getvalue()

                    # Reduce quality and try again
                    quality -= 5
                    if quality < 20:
                        # If quality is too low, resize the image
                        img = img.resize((int(img.width * 0.9), int(img.height * 0.9)))
                        quality = 95

            # Example usage
            input_bytes = b'...'  # Your image bytes here
            resized_bytes = resize_image_bytes(input_bytes)"""

            logging.info("file is bigger than 10MB. skipping!")

    async def enqueue(self, **kwargs) -> None:
        await self.repository.enqueue_sending_picture(item=self.send_photo, **kwargs)
        logging.info("enqueued photo to %s", kwargs['chat_id'])
