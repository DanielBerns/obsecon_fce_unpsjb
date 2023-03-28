"""
Bot to get Telegram messages.

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
import logging
import os
import subprocess
import shlex

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


from core import (start_filesystem, 
                  get_token, 
                  data_path, update_code_path)
from treestore import TreeStore

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# The [ExtBot, dict, dict, dict] is for type checkers like mypy
class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):

    def __init__(self, application: Application, chat_id: int = None, user_id: int = None):
        super().__init__(application=application, chat_id=chat_id, user_id=user_id)
        self._treestore = TreeStore(data_path, 'messages')

    @property
    def treestore(self) -> TreeStore:
        return self._treestore



async def start(update: Update, context: CustomContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: CustomContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def process_text(update: Update, context: CustomContext) -> None:
    """Process text message."""
    if update.message:
        if update.message.text:
            sample = context.treestore.new_sample()
            logger.info(f"Created sample {str(sample):s}!")            
            # Log text
            user = update.effective_user
            logger.info(
                f"Found text {update.message.text:s} from {user.full_name:s}")
            await update.message.reply_text(f"Text: {update.message.text:s} from {user.full_name:s}")
        else:
            # None
            logger.info("Not found update.message.text!")
            await update.message.reply_text("None")
    else:
        logger.info("Not found update.message!")


async def process_photo(update: Update, context: CustomContext) -> None:
    """Process photo message."""
    if update.message:
        if update.message.photo:
            sample = context.treestore.new_sample()
            logger.info(f"Created sample {str(sample):s}!")           
            file_id = update.message.photo[-1].file_id
            new_file = await context.bot.get_file(file_id)
            image_id = Path(sample, 'photo.jpeg')
            await new_file.download_to_drive(image_id)
            # Log photo
            user = update.effective_user
            remark = ["Found photo: ",
                      f"PhotoSize == {len(update.message.photo):d} ",
                      f"image_id = {str(image_id):s} ",
                      f"from {user.full_name:s}!"]
            logger.info(''.join(remark))            
            if update.message.caption:
                # Log caption
                logger.info(f"Found caption {update.message.caption:s}!")
            else:
                # None
                logger.info("Not found update.message.caption!")
            
            await update.message.reply_text(f"Photo from {user.full_name:s}")
        else:
            # None
            logger.info("Not found update.message.photo!")
            await update.message.reply_text("No photo nor caption")
    else:
        logger.info("Not found update.message!")


async def shutdown(update: Update, context: CustomContext) -> None:
    logger.info(f"PID {os.getpid():d}")
    flag = context.bot_data.get('shutdown', False)
    if flag:
        logging.info("pending shutdown")
        await update.message.reply_text("pending shutdown")            
        return
    logging.info("start shutdown")
    await update.message.reply_text("start shutdown")    
    context.bot_data['shutdown'] = True
    # https://phoenixnap.com/kb/linux-at-command
    command = f"#!/usr/bin/env bash\nkill {os.getpid():d}\n"
    command_path = Path(data_path, 'shutdown').with_suffix('.sh')
    with open(command_path, 'w') as target:
        target.write(command)
    os.chmod(command_path, 0o700)
    cp = subprocess.run(["at", "now", "+1", "minutes", "-f", str(command_path),])
    if cp.returncode:
        logging.info(f"at returncode {cp.returncode:d}")
    logging.info("executing shutdown")    
    await update.message.reply_text("executing shutdown")    

async def _update_code() -> None:
   cwd = os.getcwd()
   os.chdir(update_code_path)
   cp = subprocess.run(["git", "pull"])
   os.chdir(cwd)

async def update_code(update: Update, context: CustomContext) -> None:
    flag = context.bot_data.get('update_code', False)
    if flag:
        logging.info("updating code")
        await update.message.reply_text("updating code")            
        return
    logging.info("start code update")
    await update.message.reply_text("start code update")    
    context.bot_data['update_code'] = True
    await _update_code()
    context.bot_data['update_code'] = False
    if cp.returncode:
        logging.info(f"returncode {cp.returncode:d}")
    logging.info("end code update")    
    await update.message.reply_text("end code update")

def main() -> None:
    """Start the bot."""
    start_filesystem()
    context_types = ContextTypes(context=CustomContext)
    builder = Application.builder()
    builder.token(get_token())
    builder.context_types(context_types)    
    application = builder.build()

    logger.info(f"PID {os.getpid():d}")
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("shutdown", shutdown))
    # testing this
    application.add_handler(CommandHandler("uc", update_code))
    
    
    # on non commands 
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, process_text)
    )
    application.add_handler(
        MessageHandler(filters.PHOTO & ~filters.COMMAND, process_photo)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
