from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container
import components.telegram_agent as telegram
import components.twitter_agent as twitter


def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()

    
def main():
    fs = Config.FILESYSTEM
    create_metadata(fs)
    telegram.get_secrets(fs.secrets)
    twitter.get_secrets(fs.secrets)
    

if __name__ == '__main__':
    main()
