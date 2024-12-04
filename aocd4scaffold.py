with open('day4input.txt', 'r') as f:
    filegrid = f.read().splitlines()
def rowscan(text: str, quarry: str) -> int:
    return text.count(quarry)

def get_column(data: list, column_index: int) -> str:
    return ''.join(row[column_index] for row in data)

def get_diagonal(row: int, col: int, dire: str = "forward", spread: int = 4) -> str:
    _x = x 
    _y = y 
    strbuf = [] 
    _row = row
    _col = col 
    _dir = dire    
    if _dir == "forward" and spread == 4:
        while _row < _x and _col < _y:     
            strbuf.append(grid[_row][_col])
            _row += 1                      
            _col += 1                      
        return ''.join(strbuf) 
    elif _dir == "backward" and spread == 4:
        while _row < _x and _col >= 0:
            strbuf.append(grid[_row][_col])
            _row += 1
            _col -= 1
        return ''.join(strbuf)
    return 42
  
def lazy_check_square(row: int, col:int) -> int:
    if not grid[row][col] == "A":
        return 0
    count = 0
    assert not row == 0
    assert not col == 0
    TL = grid[row-1][col-1]
    TR = grid[row-1][col+1]
    BR = grid[row+1][col+1]
    BL = grid[row+1][col-1]
    if (TL + TR == "MM" and BL + BR == "SS"):
        count += 1
    elif (TL + TR == "SS" and BL + BR == "MM"):
        count += 1
    elif (TL + TR == "SM" and BL + BR == "SM"):
        count += 1
    elif (TL + TR == "MS" and BL + BR == "MS"):
        count += 1
    return count

def do_part_one() -> int:
    xmascount = 0
    for row in grid:
        xmascount += rowscan(row, word) 
        xmascount += rowscan(row, word[::-1]) 

    for i in range(x):
        col = get_column(grid, i) 
        xmascount += rowscan(col, word) 
        xmascount += rowscan(col, word[::-1]) 

    for start_x in range(x):
        temp = get_diagonal(start_x,0,"forward") 
        xmascount += rowscan(temp, word)
        xmascount += rowscan(temp, word[::-1])

    for start_y in range(1,y):
        temp = get_diagonal(0,start_y,"forward")
        xmascount += rowscan(temp, word)
        xmascount += rowscan(temp, word[::-1])
        
    for start_x in range(x):
        temp = get_diagonal(start_x, x-1 ,"backward")
        xmascount += rowscan(temp, word)
        xmascount += rowscan(temp, word[::-1])
        
    for start_y in (range(0,y-1)):   
        temp = get_diagonal(0,start_y,"backward")
        xmascount += rowscan(temp, word)
        xmascount += rowscan(temp, word[::-1])
        
    return xmascount

def do_part_two() -> int:
    p2xmascount = 0
    _grid = grid
    MAX_COL = len(_grid[0]) - 1
    MAX_ROW = len(_grid) - 1
    for row in range(1,MAX_ROW):
        for column in range(1,MAX_COL):
            if _grid[row][column] == "A":
                p2xmascount += lazy_check_square(row,column)            
    return p2xmascount

grid = filegrid
x = len(grid[0])
y = len(grid)
word = "XMAS"
assert word[::-1] == "SAMX"
xmascount=do_part_one()
part2xmascount=do_part_two()
print("part 1: ", str(xmascount))
print("part 2: ", str(part2xmascount))
