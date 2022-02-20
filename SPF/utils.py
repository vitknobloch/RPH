'''
Module for reading and writing files with classification
'''
def read_classification_from_file(filepath):
    '''
    Loads classification from file and returns dictionary of 'file':'class'
    Params:
    filepath: relative or absolute path of the classification file
    '''
    files_dict = dict()

    with open(filepath, mode="r", encoding="utf-8") as file:
        for line in file:
            data = line.rstrip().split(' ', maxsplit=2)
            files_dict[data[0]] = data[1]

    return files_dict


def write_classification_to_file(class_dict, filepath):
    '''
    Writes classification from dictionary of 'file':'class' to file
    Params:
    class_dict: dictionary of 'file':'class
    filepath: relative or absolute path of the classification file to write
    '''
    with open(filepath, mode="w", encoding="utf-8") as file:
        for key in class_dict:
            file.write(f'{key} {class_dict[key]}\n')



if __name__ == '__main__':
    files_dict = read_classification_from_file('data/3/!truth.txt')

    write_classification_to_file(files_dict, 'data/1/!prediction.txt')
