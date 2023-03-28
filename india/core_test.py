import random
import core
from helpers import save_json, get_container, get_resource_identifier

def create_metadata(fs: core.FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = core.Metadata(container)
    metadata.start()
    metadata.add_value('download', '20221118', {'stage': 'raw'})
    metadata.add_value('download', '20221119', {'stage': 'raw'})    
    metadata.add_value('download', '20221120', {'stage': 'raw'})
    metadata.stop()


def read_metadata(fs: core.FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = core.Metadata(container)
    metadata.start()

    print('Original')
    for first_key, second_key, sample in metadata.get_values():
        print(first_key, ' - ', second_key)
        for attribute, value in sample.items():
            print('  ', attribute, ' - ', value)
    metadata.events['download']['20221118']['process'] = 'alpha'
    metadata.events['download']['20221119']['process'] = 'bravo'
    metadata.events['download']['20221120']['process'] = 'charlie'
    print('Modified')
    for first_key, second_key, sample in metadata.get_values():
        print(first_key, ' - ', second_key)
        for attribute, value in sample.items():
            print('  ', attribute, ' - ', value)    


import pdb

def create_json_document(fs: core.FileSystem) -> None:
    pdb.set_trace()    
    container = get_container(fs.data, 'json_document')
    document = core.JSONDocument(container)
    document.start()
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(10):
        event = {}
        for j in range(5):
            key = ''.join([c for c in random.choices(letters, k=10)])
            value = ''.join([c for c in random.choices(letters, k=10)])
            event[key] = value
        document.add_value(event)
    document.stop()    


def read_json_document(fs: core.FileSystem) -> None:
    pdb.set_trace()        
    container = get_container(fs.data, 'json_document')
    document = core.JSONDocument(container)
    document.start()
    print(str(document.store))
    for value in document.get_values():
        print(value)
        # for k, v in value.items():
        #    print('  ', k, v)
    document.stop()    
    
def main():
    fs = core.FileSystem('india', '1')    
    fs.clear()
    create_metadata(fs)
    read_metadata(fs)
    create_json_document(fs)
    read_json_document(fs)    

if __name__ == '__main__':
    main()
