rows = [[1.0, 2.0, 4.0, -7.0],
        [2.0, 4.0, 6.0, -10.0],
        [4.0, 6.0, 8.0, -16.0]]

def make_em(rows, pivot):
    # if the pivot is at the second to the last column of the matrix, we are done
    if pivot[1] == len(rows[0]) - 2:
        return rows

    # make sure pivot is non-zero, swapping rows as necessary
    row_addition = 1
    while rows[pivot[0]][pivot[1]] == 0:
        # if we have reached the end of the rows, move pivot over a column since this column is all zeros
        if pivot[0] == len(rows) - 1:
            return make_em(rows, [pivot[0], pivot[1] + 1])
        # see if the next row down is not zero
        option_row = rows[pivot[0] + row_addition][pivot[1]]
        if not option_row == 0:
            swap_row = rows.pop(pivot[0] + row_addition)
            rows.insert(pivot[0], swap_row)
        row_addition += 1

    # make column below pivot be zero
    for row_index in range(pivot[0] + 1, len(rows)):
        # iterate through every row below the pivot, setting the scale as -below_pivot / pivot
        scale = -rows[row_index][pivot[1]] / rows[pivot[0]][pivot[1]]
        # go through every column beyond the pivot, adding scale*row above to what is there
        for column_index in range(pivot[1], len(rows[0])):
            rows[row_index][column_index] = rows[row_index][column_index] + scale * rows[pivot[0]][column_index]

    # perform the same steps on the sub-matrix made by moving pivot down and to the right
    # but only if we are not on the last row of the matrix
    if pivot[0] == len(rows):
        return rows
    else:
        return make_em(rows, [pivot[0] + 1, pivot[1] + 1])

def make_rem(rows, pivot):

    #make sure pivot is as far to the left of the matrix as possible
    while not pivot[1] == 0 and not rows[pivot[0]][pivot[1] - 1] == 0:
        pivot[1] -= 1

    # make values of the column above be zero
    for row_index in range(0, pivot[0]):
        scale = -rows[row_index][pivot[1]] / rows[pivot[0]][pivot[1]]
        for column_index in range(len(rows[0])):
            rows[row_index][column_index] = rows[row_index][column_index] + scale * rows[pivot[0]][column_index]

    # scale row by the value of the pivot
    pivot_val = rows[pivot[0]][pivot[1]]
    for column_index in range(len(rows[0])):
        rows[pivot[0]][column_index] /= pivot_val

    # if we have reached the first row of the matrix, we are done
    if pivot[0] == 0:
        return rows

    # otherwise, move the pivot up a row
    return make_rem(rows, [pivot[0] - 1, pivot[1]])

answer = make_em(rows, [0,0])
answer = make_rem(answer, [len(rows) - 1, len(rows[0]) - 2])
for row in answer:
    print(row)