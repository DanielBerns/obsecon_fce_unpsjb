"""
Agent able to manage Telegram messages.

First, a few handler functions are defined. 
Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Based in Echobot example, acknowledges messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from pathlib import Path
import os
import subprocess
import shlex
import json
from typing import Dict, Optional, Union
import logging

from components.helpers import get_timestamp

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update

from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ExtBot,
    filters,
)

from components.core import TreeStore
from components.helpers import get_resource


# The [ExtBot, dict, dict, dict] is for type checkers like mypy
class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    telegram_home: Optional[Path] = None
    store: Optional[TreeStore] = None
    shutdown_sh: Optional[Path] = None
    update_repo_sh: Optional[Path] = None
    
    def __init__(
        self, 
        application: Application, 
        chat_id: int = None, 
        user_id: int = None
        ) -> None:
        super().__init__(application=application, chat_id=chat_id, user_id=user_id)


async def start(update: Update, context: CustomContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CustomContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "/inicio, /ayuda, /telegram, /noticias"
    )


async def get_telegram(update: Update, context: CustomContext) -> None:
    """Send a message when the command /telegram is issued."""
    logging.debug("get_telegram 1")    
    ts = CustomContext.store
    logging.debug(f"get_telegram 2: {ts.index:d}")
    await update.message.reply_text(f"telegram {ts.index:d}")


async def get_websites(update: Update, context: CustomContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("noticias")


class TelegramSample:

    @staticmethod
    def get_message_id(sample: Path) -> Path:
        return Path(sample, "message").with_suffix(".txt")
        
    @staticmethod
    def get_image_id(sample: Path) -> Path:
        return Path(sample, "photo.jpeg")

    @staticmethod
    def get_caption_id(sample: Path) -> Path:
        return Path(sample, "caption").with_suffix(".txt")

    @staticmethod    
    def write_message(
        sample: Path, 
        user_full_name: str, 
        message_text: str
        ) -> None:
        logging.debug("write_message: 0")
        message_id = TelegramSample.get_message_id(sample)
        logging.debug("write_message: 1")
        with open(message_id, "w") as target:
            logging.debug("write_message: 2")            
            target.write(f"{user_full_name:s}:{message_text:s}\n")
        logging.debug("write_message: 3")
        
    @staticmethod
    def write_message_caption(
        sample: Path, 
        user_full_name: str, 
        message_caption: str
        ) -> None:
        caption_id = TelegramSample.get_caption_id(sample)
        with open(caption_id, "w") as target:
            target.write(f"{user_full_name:s}:{message_caption:s}\n")


async def process_text(update: Update, context: CustomContext) -> None:
    """Process text message."""
    if update.message:
        if update.message.text:
            ts = CustomContext.store
            ts.start()
            sample = ts.create_sample()
            ts.stop()
            logging.info(f"Created sample {str(sample):s}!")            
            TelegramSample.write_message(
                sample, 
                update.effective_user.full_name, 
                update.message.text)
            await update.message.reply_text(
                f"Gracias por tu mensaje {update.effective_user.full_name:s}!"
            )
        else:
            # None
            logging.info("Not found update.message.text!")
            await update.message.reply_text("None")
    else:
        logging.info("Not found update.message!")


async def process_photo(update: Update, context: CustomContext) -> None:
    """Process photo message."""
    if update.message:
        if update.message.photo:
            ts = CustomContext.store
            ts.start()
            sample = ts.create_sample()
            ts.stop()
            logging.info(f"Created sample {str(sample):s}!")
            file_id = update.message.photo[-1].file_id
            new_file = await context.bot.get_file(file_id)
            image_id = TelegramSample.get_image_id(sample)
            await new_file.download_to_drive(image_id)
            # Log photo
            user = update.effective_user
            remark = [
                "Found photo: ",
                f"PhotoSize == {len(update.message.photo):d} ",
                f"image_id = {str(image_id):s} ",
                f"from {user.full_name:s}!",
            ]
            logging.info("".join(remark))
            if update.message.caption:
                # Log caption
                logging.info(f"Found caption {update.message.caption:s}!")
                TelegramSample.write_message_caption(
                    sample, 
                    user.full_name, 
                    update.message.caption)
            else:
                # None
                logging.info("Not found update.message.caption!")
            await update.message.reply_text(f"Gracias por la foto {user.full_name:s}!")
        else:
            # None
            logging.info("Not found update.message.photo!")
            await update.message.reply_text("No pude recibir la foto!")
    else:
        logging.info("Not found update.message!")


async def shutdown(update: Update, context: CustomContext) -> None:
    logging.info(f"PID {os.getpid():d}")
    flag = context.bot_data.get("shutdown", False)
    if flag:
        logging.info("pending shutdown")
        await update.message.reply_text("pending shutdown")
        return
    logging.info("start shutdown")
    await update.message.reply_text("start shutdown")
    context.bot_data["shutdown"] = True
    # https://phoenixnap.com/kb/linux-at-command
    command = f"#!/usr/bin/env bash\nkill {os.getpid():d}\n"
    logging.info(command)
    command_path = CustomContext.shutdown_sh
    logging.info(str(command_path))
    with open(command_path, "w") as target:
        target.write(command)
    os.chmod(command_path, 0o700)
    cp = subprocess.run(
        [
            "at",
            "now",
            "+1",
            "minutes",
            "-f",
            str(command_path),
        ]
    )
    if cp.returncode:
        logging.info(f"at returncode {cp.returncode:d}")
    logging.info("executing shutdown")
    await update.message.reply_text("executing shutdown")


async def _update_repo() -> None:
    cp = subprocess.run([CustomContext.update_repo_sh])
    if cp.returncode:
        logging.info(f"returncode {cp.returncode:d}")


async def update_repo(update: Update, context: CustomContext) -> None:
    flag = context.bot_data.get("update_repo", False)
    if flag:
        logging.info("updating repo")
        await update.message.reply_text("updating repo")
    else:
        logging.info("start repo update")
        await update.message.reply_text("start repo update")
        context.bot_data["update_repo"] = True
        await _update_repo()
        context.bot_data["update_repo"] = False
        logging.info("end repo update")
        await update.message.reply_text("end repo update")


def run(
    telegram_home: Path, 
    telegram_token: str,
    update_repo_sh: Path) -> None:

    store = TreeStore(telegram_home, "messages")
    if CustomContext.telegram_home is None:
        CustomContext.telegram_home = telegram_home
    if CustomContext.store is None:
        CustomContext.store = store
    if CustomContext.shutdown_sh is None:
        CustomContext.shutdown_sh = get_resource(telegram_home, "shutdown", ".sh")
    if CustomContext.update_repo_sh is None:
        CustomContext.update_repo_sh = update_repo_sh        
    context_types = ContextTypes(context=CustomContext)
    builder = Application.builder()
    builder.token(telegram_token)
    builder.context_types(context_types)
    application = builder.build()

    logging.info(f"PID {os.getpid():d}")
    application.add_handler(CommandHandler("inicio", start))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(CommandHandler("telegram", get_telegram))
    application.add_handler(CommandHandler("noticias", get_websites))
    application.add_handler(CommandHandler("sd", shutdown))
    application.add_handler(CommandHandler("ur", update_repo))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_text)
    )
    application.add_handler(
        MessageHandler(filters.PHOTO & ~filters.COMMAND, process_photo)
    )

    logging.debug(f"start: {get_timestamp():s}")
    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    logging.debug(f"stop: {get_timestamp():s}")
