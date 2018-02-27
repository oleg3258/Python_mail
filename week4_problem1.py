import os
import tempfile


class File:
    def __init__(self, filepath):
        self.file = filepath
        self.k = 0

    def write(self, string):
        with open(self.file, 'a') as f:
            f.write(string)

    def __str__(self):
        return '{}'.format(self.file)

    def __add__(self, obj):
        storage_path = os.path.join(tempfile.gettempdir(), 'two_files.txt')
        new_class = File(storage_path)
        with open(new_class.file, 'w') as f:
            with open(self.file) as f1:
                for line in f1:
                    f.write(line)
            with open(obj.file) as f2:
                for line in f2:
                    f.write(line)
            return new_class

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file, 'r') as f:
            file_string = f.readlines()
        if (self.k < len(file_string)):
            res = self.k
            self.k += 1
            return file_string[res].rstrip()
        else:
            raise StopIteration()


# first = File("first.txt")
# first.write('file number one\n')
#
# second = File("second.txt")
# second.write('file number two\n')
#
# new_obj = first + second
#
# for line in File(new_obj.file):
#     print (line)