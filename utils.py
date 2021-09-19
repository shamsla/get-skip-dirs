import os
import json


def getSchema():
    with open('schema.json', "r") as schema_file:
        try:
            schema = checkSchema(json.load(schema_file))
            if not schema:
                raise Exception()
            return schema
        except:
            print('\n\tInvalid schema.json')
            input('\npress enter to exit ...')
            exit()


def checkSchema(schema):
    defaults = {'dirs': [], 'ext': [], 'files': []}

    if not type(schema) == dict:
        return False

    if 'dirs' in schema and type(schema['dirs']) == list:
        defaults['dirs'] = schema['dirs']

    if 'ext' in schema and type(schema['ext']) == list:
        defaults['ext'] = ['.' + str(ext) if ext[0] != '.' else str(ext)
                           for ext in schema['ext']]

    if 'files' in schema and type(schema['files']) == list:
        defaults['files'] = schema['files']

    return defaults


def convertBytes(_bytes):
    if _bytes < 1000:
        return f"{_bytes} Bytes"
    elif _bytes < 1000**2:
        return f"{_bytes / 1000} KB"
    elif _bytes < 1000**3:
        return f"{_bytes/1000**2} MB"
    elif _bytes < 1000**4:
        return f"{_bytes/1000**3} GB"
    elif _bytes < 1000**5:
        return f"{_bytes/1000**4} TB"
    else:
        return f"{_bytes}"


def askPath(message, dot=False):
    path = input(message)

    if path == '0':
        exit()

    # dot=self.source means if the user input == '.' then set self.destination = parent_of_self.source to create the copy_folder in the same path where the source folder is located
    if dot and path == '.':
        return dot

    if path == '.' or not os.path.exists(path) or not os.path.isdir(path):

        print('\n\tInvalid Path!\n')
        return askPath(message)

    return path


def getFilesSize(path_name, files):
    size_of_files = 0

    for _file in files:
        size_of_files += os.stat(joinPath(path_name, _file)).st_size

    return size_of_files


def joinPath(p1, p2):
    return os.path.join(p1, p2)
