import random


from components.config import Config
from components.core import FileSystem
from components.helpers import save_json, get_container, get_resource_identifier

def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = core.Metadata(container)
    metadata.start()
    metadata.add_item('download', '20221118', {'stage': 'raw'})
    metadata.add_item('download', '20221119', {'stage': 'raw'})    
    metadata.add_item('download', '20221120', {'stage': 'raw'})
    metadata.stop()


def read_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = core.Metadata(container)
    metadata.start()
    print('Original')
    for first_key, second_key, sample in metadata.items():
        print(first_key, ' - ', second_key)
        for attribute, value in sample.items():
            print('  ', attribute, ' - ', value)
    metadata.events['download']['20221118']['process'] = 'alpha'
    metadata.events['download']['20221119']['process'] = 'bravo'
    metadata.events['download']['20221120']['process'] = 'charlie'
    print('Modified')
    for first_key, second_key, sample in metadata.items():
        print(first_key, ' - ', second_key)
        for attribute, value in sample.items():
            print('  ', attribute, ' - ', value)    

class EventSource:
    def __init__(self):
        self._store = None
        
    @property
    def store(self):
        return self._store
    
    @store.setter
    def store(self, value):
        self._store = value

    def events(self):
        for e in self.store:
            yield e

def create_event():
    letters = 'abcdefghijklmnopqrstuvwxyz'    
    event = {}
    for j in range(5):
        key = ''.join([c for c in random.choices(letters, k=10)])
        value = ''.join([c for c in random.choices(letters, k=10)])
        event[key] = value
    return event

def create_json_document(fs: FileSystem) -> None:
    container = get_container(fs.data, 'json_document')
    document = core.JSONDocument(container)
    document.start()
    es = EventSource()
    es.store = [create_event() for i in range(10)]
    document.update(es)
    document.stop()    


def read_json_document(fs: FileSystem) -> None:
    container = get_container(fs.data, 'json_document')
    document = core.JSONDocument(container)
    document.start()
    print(str(document.store))
    for value in document.events():
        print(value)
        # for k, v in value.items():
        #    print('  ', k, v)
    document.stop()    
    
def main():
    fs = Config.FILESYSTEM
    fs.clear()
    create_metadata(fs)
    read_metadata(fs)
    create_json_document(fs)
    read_json_document(fs)    

if __name__ == '__main__':
    main()
