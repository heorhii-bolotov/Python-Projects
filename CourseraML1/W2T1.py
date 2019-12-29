"""
    Линейная алгебра: сходство текстов

    Дан набор предложений, скопированных с Википедии. Каждое из них имеет "кошачью тему" в одном из трех смыслов:

      -   кошки (животные)
      -   UNIX-утилита cat для вывода содержимого файлов
      -   версии операционной системы OS X, названные в честь семейства кошачьих

    file:
        cat_sentences.txt

"""


import os
from tempfile import gettempdir
from re import findall
from numpy import zeros
from collections import OrderedDict
from scipy.spatial.distance import cosine


"""
Суть следующая:
    
Генерируете матрицу нулей размера число_строк*число уникальных_слов
Вы запускаете цикл по строкам, значение строки заносите в счётчик i
В каждой строке вы запускаете цикл по словам в строке.
Если слово встречается 1й раз в строке заносите в переменную count 1 (count =1).
Если не первый, то прибавляете 1 (count +=1).
Используете полученное слово (из строки) в качестве КЛЮЧА для словаря, чтобы получить ИНДЕКС.
ИНДЕКС используете, как j для внесения значения числа вхождений в строку слова в матрицу (matrix[i,j] = count)
"""


data_file = "/Users/macair/Python Projects/CourseraML1/cat_sentences.txt"
new_file = "/Users/macair/Desktop/data.txt"


def run_operation():
    data = Data()

    matrix = Matrix(data)
    array2 = matrix.get_data_matrix(data_file)

    indices = distance_cosine(array2, 0, 2)

    file = os.path.join(gettempdir(), ".submission-1.txt")

    data.write_data(file, *indices)


class Matrix:
    def __init__(self, data_obj):
        self.Data = data_obj

    @staticmethod
    def get_default_matrix(row, column):
        return zeros((row, column), dtype=int)

    def get_data_matrix(self, data_file):

        # Unique words
        all_words = self.Data.extract_data(data_file)

        # Get row/column size of matrix
        sizes = self.Data.get_row_cols_num()

        # Default matrix
        matrix = self.get_default_matrix(*sizes)

        # Read each line
        for row, line in enumerate(self.Data.read_by_line(data_file)):

            # Extract all words from line
            words = findall(r"\w+", line.lower())

            for word in words:

                # Get word column-index
                column = all_words.get(word, 0)

                # Entry number
                matrix[row, column] += 1

        # Matrix with words entries
        return matrix


class Data:

    # row(lines) and column(words) counters
    _r_counter = 0
    _c_counter = 0

    def get_row_cols_num(self):
        return self._r_counter, self._c_counter
    
    @staticmethod
    def read_by_line(data_file):

        with open(data_file, "r") as file:
            for line in file:

                yield line

    @staticmethod
    def write_data(data_file=None, *args):

        # Make temporary directory file
        temp = os.path.join(gettempdir(), f".{hash(os.times())}")

        # Make file
        os.makedirs(temp)

        with open(data_file or temp, "w") as file:

            # Concatenate data
            data = " ".join(list(map(str, args)))

            file.write(data)

    def extract_data(self, data_file):

        # Return all extracted words
        all_words = OrderedDict()

        # Row/column counters
        r_counter, c_counter = 0, 0

        # Read data by each line
        for line in self.read_by_line(data_file):

            # Extract all words from line
            words = findall(r"\w+", line.lower())

            for word in words:

                # If new word
                if all_words.get(word, None) is None:

                    # Add new word
                    all_words[word] = c_counter

                    # Columns counter
                    c_counter += 1

            # Row counter
            r_counter += 1

        # Number of lines/words, rows/columns
        self._r_counter, self._c_counter = r_counter, c_counter

        # Unique words in dict
        return all_words


def distance_cosine(matrix, point=0, nums=1):

    # Get cosine distances between point and other sentences
    distances = {num: cosine(matrix[point], row) for num, row in enumerate(matrix)}

    # Get from 1 to nums nearest distances
    nearest_pairs = sorted(distances.items(), key=lambda kv: kv[1])[1: nums + 1]

    # First tuple contains indices
    return list(zip(*nearest_pairs))[0]


run_operation()