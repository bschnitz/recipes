import functools

def markdown_table_str(rows):
    if len(rows) == 0: return ''

    ncols = len(rows[0])
    icols = range(ncols)

    max_colsizes = lambda sizes, row: [max(len(row[i]), sizes[i]) for i in icols]
    colsizes = functools.reduce(max_colsizes, rows, [0] * ncols)

    justify = lambda row: [row[i].ljust(colsizes[i]) for i in icols]
    justified = list(map(justify, rows))

    # separator between header and body
    justified.insert(1, ['-'*size for size in colsizes])

    lines = ['|'+'|'.join(row)+'|' for row in justified]

    return '\n'.join(lines)
