
def deep_copy(l):
    if not isinstance(l, list):
        return l
    return list(
        map(deep_copy, l)
    )


def is_scalar(obj):
    return isinstance(obj, (int, float))


def is_matrix(obj):
    return isinstance(obj, Matrix)


def try_to_copy(value):
    try:
        return deep_copy(value)
    except:
        return value


class Matrix:
    """
    >>> a_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    >>> a = Matrix(3, 3, a_list)
    >>> b_list = [[2, 2, 2], [2, 2, 2], [2, 2, 2]]
    >>> b = Matrix(3, 3, b_list)
    >>> c = a + b
    >>> assert c.value == [[2, 3, 4], [5, 6, 7], [8, 9, 10]]
    """
    def __init__(self, rows: int, columns: int, value=None, **kwargs):
        self.rows = rows
        self.columns = columns
        self.value = try_to_copy(value)
        self.column_range = kwargs.get('column_range', None) or list(range(0, self.columns))
        self.row_range = kwargs.get('row_range', None) or list(range(0, self.rows))

    def map_value(self, map_fn, your_value):
        this_value = self.value
        target = self.copy()
        col_range = self.column_range
        if is_matrix(your_value):
            value = your_value.value
            for row in self.row_range:
                for column in col_range:
                    target.value[row][column] = map_fn(this_value[row][column], value[row][column])
        elif is_scalar(your_value):
            for row in self.row_range:
                for column in col_range:
                    target.value[row][column] = map_fn(this_value[row][column], your_value)
        return target

    def copy(self):
        return Matrix(
            self.rows,
            self.columns,
            value=self.value,
            column_range=self.column_range.copy(),
            row_range=self.row_range.copy()
        )

    def __add__(self, your_value):
        return self.map_value(lambda left, right: left + right, your_value)

    def __radd__(self, your_value):
        return self.__add__(your_value)

    def __mul__(self, your_value):
        """
        Point-wise multiplication
        """
        return self.map_value(lambda left, right: left * right, your_value)

    def __rmul__(self, your_value):
        """
        Right-handed point-wise multiplication
        """
        return self.__mul__(your_value)

    def __matmul__(self, your_value):
        """
        Matrix-matrix multiplication
        """
        target = self.copy()
        target_value = target.value
        if is_matrix(your_value):
            col_range = self.column_range
            row_range = self.row_range
            value = your_value.value
            # Multiply the elements in the row A of Matrix M
            # and the elements in column A of Matrix T
            for row in row_range:
                for column in col_range:
                    accum = 0
                    for reflection in row_range:
                        accum += target_value[row][reflection] * value[reflection][column]
                    target.value[row][column] = accum
        return target

    def __str__(self):
        rows = []
        for row in self.value:
            row_numbers = ', '.join(
                list(map(str, row))
            )
            rows.append('({})'.format(row_numbers))
        matrix_rows = ', \n    '.join(rows)
        return """[\n    {}\n]""".format(matrix_rows)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.value[key[0]][key[1]]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            self.value[key[0]][key[1]] = value
