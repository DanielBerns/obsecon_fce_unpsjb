from components.config import Config
import components.telegram_agent as telegram
import components.twitter_agent as twitter


def create_metadata(fs: core.FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = core.Metadata(container)
    metadata.start()
    metadata.stop()

    
def main():
    fs = Config.FILESYSTEM
    create_metadata(fs)
    telegram.get_secrets(fs.secrets)
    twitter.get_secrets(fs.secrets)
    

if __name__ == '__main__':
    main()
