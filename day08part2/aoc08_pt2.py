"""find the tree with the highest scenic score"""

from functools import reduce
import pandas as pd

# take text file convert into
# a list of lists of integers
with open("input08.txt", encoding='utf-8') as f:
    lines = f.read().splitlines()
data = [list(i) for i in lines]
data = [[int(j) for j in i] for i in data]
df = pd.DataFrame(data)
side = df.shape[0] - 1  # length of one side - 1 for zero based indexing
top_score = 0


def count_trees(trees, tree):
    """ take a list of trees and
    see how many can be seen from tree"""
    if len(trees) == 0:
        return 0
    view = 0
    for height in trees:
        if height >= tree:
            view += 1
            break
        else:
            view += 1
    return view


def get_views(row, col, tree):
    """given the row and col of the passed in tree
    generate a list of trees for each direction
    (i.e. below, to the right, above and to the left) then
    take each of those lists along with the tree being evaluated and
    pass them to the count_trees function
    """
    # count trees below
    if row == side:
        down = []
    else:
        down = df.iloc[row + 1:, [col]].squeeze().tolist()
        if isinstance(down, int):
            down = [down]
    d = count_trees(down, tree)

    # count trees to the right
    if col == side:
        right = []
    else:
        right = df.iloc[[row], col + 1:].squeeze().tolist()
        if isinstance(right, int):
            right = [right]
    r = count_trees(right, tree)

    # count trees above
    if row == 0:
        up = []
    else:
        up = df.iloc[:row, [col]].squeeze().tolist()
        up = [up] if isinstance(up, int) else up[::-1]
    u = count_trees(up, tree)

    # count trees to the left
    if col == 0:
        left = []
    else:
        left = df.iloc[[row], :col].squeeze().tolist()
        left = [left] if isinstance(left, int) else left[::-1]
    l = count_trees(left, tree)

    return [u, l, r, d]

# iterate through each tree in the dataframe and
# pass it to the get_views function which
# will return four numbers:
# each number representing the number of trees visible in
# each direction from the tree being evaluated
for rowIdx, df_row in df.iterrows():
    for colIdx, val in df_row.items():
        curr_row = rowIdx
        curr_col = colIdx
        curr_tree = val
        # this print line is to let me know of the progress
        print(f'row: {curr_row:3} col: {curr_col:3}', end='\r')
        views = get_views(curr_row, curr_col, curr_tree)
        score = reduce(lambda a, b: a * b, views)
        if score > top_score:
            top_score = score

print(f'\nthe top score is ► {top_score}')
