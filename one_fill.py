import numpy as np
import cv2
def sort_contours(contours, x_axis_sort, y_axis_sort):
    # initialize the reverse flag
    x_reverse = False
    y_reverse = False
    if x_axis_sort == 'RIGHT_TO_LEFT':
        x_reverse = True
    if y_axis_sort == 'BOTTOM_TO_TOP':
        y_reverse = True
    
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    
    # sorting on x-axis 
    sortedByX = zip(*sorted(zip(contours, boundingBoxes),
    key=lambda b:b[1][0], reverse=x_reverse))
    
    # sorting on y-axis 
    (contours, boundingBoxes) = zip(*sorted(zip(*sortedByX),
    key=lambda b:b[1][1], reverse=y_reverse))
    # return the list of sorted contours and bounding boxes
    return (contours, boundingBoxes)
def contour_sort(a, b):
    br_a = cv2.boundingRect(a)
    br_b = cv2.boundingRect(b)

    if abs(br_a[1] - br_b[1]) <= 15:
        return br_a[0] - br_b[0]
    return br_a[1] - br_b[1]
def solve_one_fill(grid, start):
    def is_valid_move(x, y):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 1
    
    def dfs(x, y, step):
        if (x, y) in visited:
            return False
        
        visited.add((x, y))
        path.append((x, y))
        solution_grid[x][y] = step
        
        if len(path) == total_walkable_blocks:
            return True
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if is_valid_move(new_x, new_y):
                if dfs(new_x, new_y, step + 1):
                    return True
        
        path.pop()
        visited.remove((x, y))
        return False
    
    total_walkable_blocks = sum(row.count(1) for row in grid)
    visited = set()
    path = []
    
    solution_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    if dfs(start[0], start[1], 1):
        return solution_grid
    else:
        return None
def flatten_comprehension(matrix):
     return [item for row in matrix for item in row]
# # Example grid and starting position
# grid = [
#     [-1, 1, 1, 0],
#     [1, 1, 1, 0],
#     [1, 1, 1, 1],
#     [1, 1, 1, 1]
# ]

# # Find indices of -1 using np.where()
# row_indices, col_indices = np.where(np.array(grid) == -1)
# # Combine row and column indices
# indices = list(zip(row_indices, col_indices))

# start = indices[0]
# print(type(grid[0]))
# solution_grid = solve_one_fill(grid, start)
# if solution_grid:
#     for row in solution_grid:
#         print(row)
# else:
#     print("No solution found.")
