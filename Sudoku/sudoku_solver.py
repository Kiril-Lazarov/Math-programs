init_values = [
    [0, 0, 5],
    [0, 2, 7],
    [0, 4, 6],
    [0, 5, 1],
    [0, 6, 9],
    [1, 5, 9],
    [1, 8, 4],
    [2, 0, 8],
    [3, 1, 4],
    [3, 4, 1],
    [4, 1, 8],
    [4, 6, 7],
    [5, 0, 7],
    [5, 2, 1],
    [5, 3, 5],
    [5, 8, 3],
    [6, 0, 9],
    [6, 2, 6],
    [6, 4, 5],
    [6, 6, 4],
    [7, 1, 1],
    [8, 3, 3],
    [8, 7, 2],
]
matrix = [[None] * 9] * 9


def distribute_init_values(init_values):
    matrix = [[None] * 9 for _ in range(9)]

    for data in init_values:
        row, col, value = data
        matrix[row][col] = (value, False)

    return matrix


sudoku = distribute_init_values(init_values)


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


def check_to_convert_lists(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):

            if isinstance(matrix[i][j], list):
                count_zeroes = len([x for x in matrix[i][j] if x == 0])
                if count_zeroes == 8:
                    value = [x for x in matrix[i][j] if x != 0][0]
                    matrix[i][j] = (value, False)
                    update_row(i, j, matrix)
                    update_col(i, j, matrix)
                    update_cell(i, j, matrix)


def get_cells_coordinates():
    coordinates = []
    for start_row_index in [0, 3, 6]:
        for start_col_index in [0, 3, 6]:
            for cell_row_index in range(3):
                for cell_col_index in range(3):
                    m_row = start_row_index + cell_row_index
                    m_col = start_col_index + cell_col_index
                    coordinates.append([m_row, m_col])
    return coordinates


def check_to_convert_cells(matrix):
    cells_coordinates = get_cells_coordinates()
    index = 0
    flatten_cell_list = []
    for coors in cells_coordinates:

        row, col = coors

        if isinstance(matrix[row][col], list):
            flatten_cell_list += matrix[row][col]
        index += 1
        if index != 0 and index % 9 == 0:
            unique_values = set(flatten_cell_list)
            unique_values.discard(0)

            for value in unique_values:
                if flatten_cell_list.count(value) == 1:
                    for coordinates in cells_coordinates[index - 9: index]:
                        cell_row, cell_col = coordinates
                        if isinstance(matrix[cell_row][cell_col], list):
                            if value in matrix[cell_row][cell_col]:
                                matrix[cell_row][cell_col] = (value, False)

                                update_row(cell_row, cell_col, matrix)
                                update_col(cell_row, cell_col, matrix)

                                matrix[cell_row][cell_col] = tuple([value, True])

                                break
            flatten_cell_list = []


def count_lists(matrix):
    while True:
        count_list = 0
        for row in matrix:
            count_list += sum(isinstance(elem, list) for elem in row)
        if count_list == 0:
            print(f'The sudoku is solved')
            for row in matrix:
                for values in row:
                    print(values[0], end=',')
                print()
            break
        check_rows_cols_cells(sudoku)

        check_to_convert_lists(sudoku)

        check_to_convert_cells(sudoku)

        show_matrix(sudoku)


count_lists(sudoku)
