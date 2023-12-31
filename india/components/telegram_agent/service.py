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

from components.core import Secrets
from components.helpers import get_timestamp, get_container
from components.telegram_agent.telegram_sample import TelegramSample

from telegram import __version__ as TG_VER


def filename():
    return __file__[:-3]


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


def start_shutdown(command_path: str) -> None:
    command = f"#!/usr/bin/env bash\nkill {os.getpid():d}\n"
    logging.info(command)
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


def start_reboot(command_path: str) -> None:
    os.chmod(command_path, 0o700)
    cp = subprocess.run(
        [
            "at",
            "now",
            "+2",
            "minutes",
            "-f",
            str(command_path),
        ]
    )
    if cp.returncode:
        logging.info(f"at returncode {cp.returncode:d}")


def interact_with_telegram_api(
    telegram_home: Path, bot_identifier: str, authorization_token: str
) -> None:
    bot_home = get_container(telegram_home, bot_identifier)
    store = TreeStore(bot_home, "messages")
    shutdown_sh = get_resource(bot_home, "shutdown", ".sh")
    update_repo_sh = get_resource(bot_home, "update_repo", ".sh")
    reboot_sh = get_resource(bot_home, "reboot", ".sh")

    # set higher logging level for httpx to avoid all GET and POST
    # requests being logged
    logging.getLogger("httpx").setLevel(logging.INFO)

    # logger = logging.getLogger(__name__)

    logging.info(f"PID {os.getpid():d}")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("/inicio, /ayuda, /telegram, /noticias")

    async def get_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /telegram is issued."""
        logging.debug("get_telegram 1")
        value = store.index.value
        logging.debug(f"get_telegram 2: {value:d}")
        await update.message.reply_text(f"telegram {value:d}")

    async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("noticias")

    async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Process text message."""
        if update.message is None:
            logging.debug("Not found update.message!")
            response = "process_text: empty request 1"
        elif update.message.text is None:
            logging.debug("Not found update.message.text!")
            response = "process_text: empty request 2"
        else:
            store.start()
            sample = store.create_sample()
            store.stop()
            logging.info(f"Created sample {str(sample):s}!")
            user = update.effective_user
            TelegramSample.write_message(
                sample,
                f"{user.full_name:s} - {str(update.effective_chat.id):s}",
                update.message.text,
            )
            response = f"Gracias por tu mensaje {update.effective_user.full_name:s}!"
        await update.message.reply_text(response)

    async def process_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Process photo message."""
        if update.message is None:
            logging.debug("Not found update.message!")
            response = "process_photo: empty request 1"
        elif update.message.photo is None:
            logging.debug("Not found update.message.photo!")
            response = "process_photo: empty request 2"
        else:
            store.start()
            sample = store.create_sample()
            store.stop()
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
                f"from {user.full_name:s} - {str(update.effective_chat.id):s}!",
            ]
            logging.info("".join(remark))
            if update.message.caption:
                logging.info(f"Found caption {update.message.caption:s}!")
                TelegramSample.write_message_caption(
                    sample,
                    f"{user.full_name:s} - {str(update.effective_chat.id):s}",
                    update.message.caption,
                )
            else:
                logging.info("Not found update.message.caption!")
            await update.message.reply_text(f"Gracias por la foto {user.full_name:s}!")

    async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info(f"PID {os.getpid():d}")
        flag = context.bot_data.get("shutdown", False)
        if flag:
            logging.info("pending shutdown")
            await update.message.reply_text("pending shutdown")
        else:
            logging.info("start shutdown")
            await update.message.reply_text("start shutdown")
            context.bot_data["shutdown"] = True
            # https://phoenixnap.com/kb/linux-at-command
            start_shutdown(shutdown_sh)
            logging.info("executing shutdown")
            await update.message.reply_text("executing shutdown")

    async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.info(f"PID {os.getpid():d}")
        flag = context.bot_data.get("reboot", False)
        if flag:
            logging.info("pending reboot")
            await update.message.reply_text("pending reboot")
        else:
            logging.info("start reboot")
            await update.message.reply_text("start reboot")
            context.bot_data["reboot"] = True
            # https://phoenixnap.com/kb/linux-at-command
            start_reboot(reboot_sh)
            start_shutdown(shutdown_sh)
            logging.info("executing reboot")
            await update.message.reply_text("executing reboot")

    async def _update_repo() -> None:
        cp = subprocess.run([update_repo_sh])
        if cp.returncode:
            logging.info(f"returncode {cp.returncode:d}")

    async def update_repo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        flag = context.bot_data.get("update_repo", False)
        if flag:
            logging.info("updating repo")
            await update.message.reply_text("updating repo")
        else:
            logging.info("update_repo start")
            await update.message.reply_text("update_repo start")
            context.bot_data["update_repo"] = True
            await _update_repo()
            context.bot_data["update_repo"] = False
            logging.info("update_repo end")
            await update.message.reply_text("update_repo end")

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        logging.error("Exception while handling an update:", exc_info=context.error)

        # Finally, send the message
        target_id = update.effective_chat.id
        message = "Error logged"
        await context.bot.send_message(chat_id=target_id, text=message)

    builder = Application.builder()
    builder.token(authorization_token)
    application = builder.build()

    application.add_handler(CommandHandler("inicio", start))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(CommandHandler("telegram", get_telegram))
    application.add_handler(CommandHandler("noticias", get_news))
    application.add_handler(CommandHandler("sd", shutdown))
    application.add_handler(CommandHandler("ur", update_repo))
    application.add_handler(CommandHandler("rb", reboot))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_text)
    )
    application.add_handler(
        MessageHandler(filters.PHOTO & ~filters.COMMAND, process_photo)
    )

    application.add_error_handler(error_handler)

    logging.debug(f"start: {get_timestamp():s}")
    try:
        application.run_polling()
    except Exception as message:
        logging.debug(f"error: {get_timestamp():s}")
        logging.debug(f"{str(message):s}")
    logging.debug(f"stop: {get_timestamp():s}")


class ServiceException(Exception):
    pass


def run_bot(secrets_home: Path, telegram_home: Path, bot_identifier: str) -> None:
    secrets = Secrets.read(Path(secrets_home, bot_identifier))
    if len(secrets) == 0:
        message = "".join(
            [
                f"{filename():s}.run_bot({bot_identifier:s}):",
                f"no secrets at {str(secrets_home):s}",
            ]
        )
        logging.error(message)
        raise ServiceException(message)
    authorization_token = secrets.get("TELEGRAM_TOKEN", None)
    if authorization_token is None:
        message = "".join(
            [
                f"{filename():s}.run_bot({bot_identifier:s}):",
                f"no authorization_token at {str(secrets_home):s}",
            ]
        )
        logging.error(message)
        raise ServiceException(message)
    message = "".join(
        [
            f"{filename():s}.run_bot({bot_identifier:s}): ",
            "before interact_with_telegram_api",
        ]
    )
    logging.info(message)
    interact_with_telegram_api(telegram_home, bot_identifier, authorization_token)
    message = "".join(
        [
            f"{filename():s}.run_bot({bot_identifier:s}): ",
            "after interact_with_telegram_api",
        ]
    )
    logging.info(message)
