# sudoku = list(range(9))
# print(cell)
# for i in range(len(sudoku)):
#     sudoku[i] = list(range(9))
# for row in sudoku:
#     for col in row:
#         row[col] = cell


init_values = [
    [0, 1, 2],
    [0, 4, 5],
    [1, 1, 4],
    [1, 3, 1],
    [1, 5, 9],
    [2, 7, 3],
    [2, 8, 4],
    [3, 4, 3],
    [3, 5, 1],
    [4, 1, 8],
    [4, 2, 5],
    [4, 3, 9],
    [4, 7, 4],
    [5, 8, 9],
    [6, 0, 5],
    [6, 5, 7],
    [6, 6, 8],
    [6, 7, 6],
    [7, 0, 7],
    [7, 5, 6],
    [7, 6, 9],
    [7, 7, 2],
    [7, 8, 3],
    [8, 1, 6],
    [8, 2, 2],
    [8, 5, 3],

]
matrix = [[None] * 9] * 9


def distribute_init_values(init_values):
    matrix = [[None] * 9 for _ in range(9)]

    for data in init_values:
        row, col, value = data
        matrix[row][col] = (value, False)

    return matrix


sudoku = distribute_init_values(init_values)


# print(sudoku)
# [print(row) for row in sudoku]
def show_matrix(matrix):
    for row in matrix:
        for col in row:
            if isinstance(col, list):
                print('_', end=',')
            else:
                print(col[0], end=',')
        print()

def replace_nan(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] is None:
                matrix[i][j] = list(range(1, 10))

    return matrix


sudoku = replace_nan(sudoku)

show_matrix(sudoku)



def update_row(i, j, matrix):
    value = matrix[i][j][0]

    for col in range(len(matrix[i])):

        if isinstance(matrix[i][col], list):
            for index in range(len(matrix[i][col])):
                if matrix[i][col][index] == value:
                    matrix[i][col][index] = 0
                    break


def update_col(i, j, matrix):
    value = matrix[i][j][0]

    for row in range(len(matrix[i])):

        if isinstance(matrix[row][j], list):
            for index in range(len(matrix[row][j])):
                if matrix[row][j][index] == value:
                    matrix[row][j][index] = 0
                    break


def get_ranges(i, j):
    start_row_index = 0
    start_col_index = 0
    if 3 <= i < 6:
        start_row_index = 3
    elif i >= 6:
        start_row_index = 6

    if 3 <= j < 6:
        start_col_index = 3
    elif j >= 6:
        start_col_index = 6

    return start_row_index, start_col_index


def update_cell(i, j, matrix):
    value = matrix[i][j][0]
    start_row_index, start_col_index = get_ranges(i, j)
    flatten_cell = list()
    for k in range(3):
        for l in range(3):

            if isinstance(matrix[start_row_index + k][start_col_index + l], list):
                flatten_cell += matrix[start_row_index + k][start_col_index + l]
                # print(flatten_cell)
                try:
                    index = matrix[start_row_index + k][start_col_index + l].index(value)
                    matrix[start_row_index + k][start_col_index + l][index] = 0

                except:
                    pass
    flatten_cell_set = set(flatten_cell)
    for number in flatten_cell_set:
        if number != 0:
            if flatten_cell.count(number) == 1:
                for k in range(3):
                    for l in range(3):

                        if isinstance(matrix[start_row_index + k][start_col_index + l], list):

                            if number == matrix[start_row_index + k][start_col_index + l]:

                                matrix[start_row_index + k][start_col_index + l] = (number, False)


def check_rows_cols_cells(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if isinstance(matrix[i][j][0], int) and matrix[i][j][1] is False:
                update_row(i, j, matrix)
                update_col(i, j, matrix)
                update_cell(i, j, matrix)
                temp = list(matrix[i][j])
                temp[1] = True
                matrix[i][j] = tuple(temp)
        # show_matrix(matrix)
    check_to_convert_lists(sudoku)

    # for row in matrix:
    #     print(row)


def check_to_convert_lists(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if isinstance(matrix[i][j], list):
                count_zeroes = len([x for x in matrix[i][j] if x == 0])
                if count_zeroes == 8:
                    value = [x for x in matrix[i][j] if x != 0][0]
                    matrix[i][j] = (value, False)


def count_lists(matrix):
    while True:
        count_list = 0
        for row in matrix:
            count_list += sum(isinstance(elem, list) for elem in row)
        if count_list == 0:
            print(f'The sudoku is solved')
            for row in matrix:
                for values in row:
                    print(values[0],end= ',')
                print()
            break
        check_rows_cols_cells(sudoku)
        print()
        show_matrix(sudoku)
        check_to_convert_lists(sudoku)
        # check_rows_cols_cells(sudoku)
        print()
        show_matrix(sudoku)



print(count_lists(sudoku))

'''
_,2,_,_,5,_,_,_,_,
_,4,_,1,_,9,_,_,_,
_,_,_,_,_,_,_,3,4,
_,_,_,_,3,1,_,_,_,
_,8,5,9,_,_,_,4,_,
_,_,_,_,_,_,_,_,9,
5,_,_,_,_,7,8,6,_,
7,_,_,_,_,6,9,2,3,
_,6,2,_,_,3,_,_,_,
'''