import logging

from app.engine import Engine


IDENTIFIER = "start"


def main():
    engine = Engine()

    logging.basicConfig(
        filename=engine.get_logs_resource(IDENTIFIER), 
        level=engine.config.log_level)    
    
    logging.info(f"start {IDENTIFIER:s}")
    
    logging.info("<FileSystem>")
    logging.info(f":  application_home={str(engine.fs.application_home):s}")
    logging.info(f":  info_home       ={str(engine.fs.info_home):s}")    
    logging.info("</Filesystem>")
    logging.info("<Commands>")        
    engine.create_default_commands()
    logging.info("</Commands>")    
    logging.warning("THIS IS A TEST")
    logging.error("THIS IS ANOTHER TEST")
    logging.info(f"start {IDENTIFIER:s}")

if __name__ == '__main__':
    main()
