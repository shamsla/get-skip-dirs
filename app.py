import os
import shutil
import json
from random import randrange as randomRange
from utils import convertBytes, getSchema, askPath, joinPath, getFilesSize


class CopyTree:

    """
        to copy the files from a dir by excluding some specific files and folders and extensions
    """

    def __init__(self):
        """
            source : Source Dir

            destination : Destination Dir | It could be the source dir check[utils.askPath|self.execute]

            schema : a small configuration(schema.json) for excluding the files and folders
        """

        self.source = None
        self.destination = None
        self.schema = getSchema()

    def execute(self):

        # printing the schema here
        print(f'\nSchema: {self.schema}')
        print('\n\tEnter 0 to exit.\n')

        # asking the source, dest, and changing the destination
        self.source = askPath('Enter Source Path:')

        # dot=self.source means if the user input == '.' then set self.destination = parent_of_self.source to create the copy_folder in the same path where the source folder is located
        self.destination = askPath(
            'Enter Destination Path | (.) For Same Parent Path:', dot=os.path.dirname(os.path.normpath(self.source)))

        self.destination = rf"{self.destination}\{os.path.basename(self.source)}_copy_CopyTree"

        # printing the info of the dir
        ask_for_info = input(
            'Wanna get Info(It could take some more time) | y/N :')
        if ask_for_info in ('y', 'Y' 'yes', 'Yes'):
            print('\n\tGathering Information ...')
            self.getInfo()
            should_continue = input("\nEnter to Continue | 0 to exit ...")
            print()
            if should_continue != '':
                exit()

        # checking the destination folder existence
        self.checkNCreateDest()

        # Main copying Function
        # Passing the self args because of the recursion
        self.startCopying(self.source, self.destination)
        input('\nenter to exit...')

    def startCopying(self, src_dir, dst_dir):
        dir_list = os.listdir(src_dir)
        for item in dir_list:

            src_item = joinPath(src_dir, item)
            dest_item = joinPath(dst_dir, item)

            print(f'copying {src_item}...')

            # if the item is a folder then checking it in the schema and excluding
            if os.path.isdir(src_item):
                if self.validatePath(item):
                    os.mkdir(dest_item)

                    # diving deeper into the folder itself
                    self.startCopying(src_item,
                                      dest_item)
            # if the item is a file
            elif os.path.isfile(src_item):
                if self.validateFile(item):
                    shutil.copyfile(src_item, dest_item)

    def getInfo(self):
        path_data = os.walk(self.source)
        num_of_files = 0
        num_of_folders = 0
        files_size = 0
        for root, folders, files in path_data:

            # filtering only the allowed files & folders
            folders = [
                folder for folder in folders if self.validatePath(folder)]
            files = [file for file in files if self.validateFile(file)]

            num_of_folders += len(folders)
            num_of_files += len(files)

            # getting the size of files in disk
            files_size += getFilesSize(root, files)

        print(f"\n\tFolders: {num_of_folders}")
        print(f"\tFiles: {num_of_files}")

        # conveting the bytes into KB, MB, GB, TB
        print(f"\tSize: {convertBytes(files_size)}")

    def checkNCreateDest(self):
        # if the destination folder already exists then rename it a little bit then again check it by recursion

        if os.path.exists(self.destination) and os.path.isdir(self.destination):

            # adding some random stuff at the end of the path string
            self.destination = self.destination + \
                str(randomRange(561992, 6864545))

            # to check the dest again
            self.checkNCreateDest()

        else:
            # if dest already not exists then creating it
            os.mkdir(self.destination)

    def validatePath(self, _dir):
        # simply checking the folder in schema
        # if it exists then return False to exclude it
        # otherwise return True to include
        if _dir not in self.schema["dirs"]:
            return True

        return False

    def validateFile(self, _file):
        # simply checking the file in schema
        # if it exists then return False to exclude it
        # otherwise return True to include
        if os.path.splitext(_file)[1] not in self.schema["ext"] and _file not in self.schema['files']:
            return True

        return False


test = CopyTree()
test.execute()
