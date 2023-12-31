from pathlib import Path
import logging

from components.helpers import get_resource


class TelegramSample:
    @staticmethod
    def get_message_id(sample: Path) -> Path:
        return get_resource(sample, "message", ".txt")

    @staticmethod
    def get_image_id(sample: Path) -> Path:
        return get_resource(sample, "photo", ".jpeg")

    @staticmethod
    def get_caption_id(sample: Path) -> Path:
        return get_resource(sample, "caption", ".txt")

    @staticmethod
    def write_message(sample: Path, user_full_name: str, message_text: str) -> None:
        logging.debug("write_message: 0")
        message_id = TelegramSample.get_message_id(sample)
        logging.debug("write_message: 1")
        with open(message_id, "w") as target:
            logging.debug("write_message: 2")
            target.write(f"{user_full_name:s}:{message_text:s}\n")
        logging.debug("write_message: 3")

    @staticmethod
    def write_message_caption(
        sample: Path, user_full_name: str, message_caption: str
    ) -> None:
        caption_id = TelegramSample.get_caption_id(sample)
        with open(caption_id, "w") as target:
            target.write(f"{user_full_name:s}:{message_caption:s}\n")
