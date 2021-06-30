import argparse
import os
import hashlib


class Handler:

    def __init__(self, name):
        self.path = name

    def list_files(self, endwith=''):
        """List directory and subdirectory files"""
        self.path = self.path.replace('\\', '\\\\')
        if os.path.isdir(path):
            return [os.path.join(root, name) for root, dirs, files in os.walk(path, topdown=False)
                    for name in files if os.path.join(root, name).endswith(endwith)]

    def get_hash(self, path):
        """Get hash"""
        hash_md5 = hashlib.md5()
        with open(path, 'rb') as f:
            data = f.read()
        hash_md5.update(data)
        return hash_md5.hexdigest()

    def output_identical(self):
        """List of files of the same format and size"""
        f_format = input("Enter file format:\n")

        print("\nSize sorting options:\n1. Descending\n2. Ascending")
        sorting_options = True if self.question("Enter a sorting option:", "1", "2") == "1" else False
        list_files = self.list_files(f_format)
        tuple_size = sorted(list({os.path.getsize(key) for key in list_files}), reverse=sorting_options)
        same_size = {key: [x for x in list_files if os.path.getsize(x) == key] for key in tuple_size if
                     [os.path.getsize(x) for x in list_files].count(key) > 1}
        return same_size

    def output_with_hash(self, s_s):
        """Get list of files with the same hash"""
        num = 1

        for byte, hashes in s_s.items():
            print()
            print(byte, "bytes")
            for hsh, files_l in hashes.items():
                print('Hash:', hsh)
                for file_name in files_l:
                    print(f"{num}. {file_name}")
                    num += 1

    def get_hsh_dict(self, same_size):
        """Get dictionary with same hash from dictionary with same size"""
        return {size_files: {hsh: [name for name in same_size[size_files]
                                   if self.get_hash(name) == hsh]
                             for hsh in {self.get_hash(file) for file in same_size[size_files]}
                             if [self.get_hash(file) for file in same_size[size_files]].count(hsh) > 1}
                for size_files in same_size}

    def output(self):
        """Just output"""
        dict1 = self.output_identical()
        print('\n' + '\n'.join(str(key) + ' bytes' + '\n' + '\n'.join(dict1[key]) + '\n' for key in dict1))
        if self.question("Check for duplicates?", "yes", "no") == "yes":
            same_hash = self.get_hsh_dict(dict1)
            self.output_with_hash(same_hash)
        if self.question("Delete files?", "yes", "no") == "yes":
            self.delete_files([file for sublist_f in [two_list for hsh_list in same_hash.values()
                                                      for two_list in hsh_list.values()]
                               for file in sublist_f])

    def delete_files(self, files):
        """Delete files which a user want"""
        total = 0
        numbers = input("Enter file numbers to delete:\n").split()
        if numbers and all(num.isdigit() for num in numbers):
            numbers = [int(num) for num in numbers]
            if all([len(files) >= num for num in numbers]):
                for num in numbers:
                    total += os.path.getsize(files[num - 1])
                    os.remove(files[num - 1])
                print(f"Total freed up space: {total} bytes")
        else:
            print("Wrong format")

    @staticmethod
    def question(sentence, *values):
        while True:
            answer = input(f"\n{sentence}\n")
            if answer not in values:
                print("Wrong option")
            else:
                break
        return answer


parser = argparse.ArgumentParser(description='Output displays a lists files and folders in a specific directory')
parser.add_argument('path', nargs='?', type=str, help='Directory path')
path = parser.parse_args().path
if path:
    handler = Handler(path)
    handler.output()
else:
    print("Directory is not specified")
