import cv2
import numpy as np
import matplotlib.pyplot as plt
from one_fill import solve_one_fill
from one_fill import sort_contours
from one_fill import flatten_comprehension
from one_fill import contour_sort

from functools import cmp_to_key

def solve(path,reverse):
    # Load the image using OpenCV
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x1, y1, x2, y2 = 0, 200, 1000, 900
    # Crop the image to extract the ROI
    cropped_image = image[y1:y2, x1:x2]

    # Apply Canny edge detection
    edges = cv2.Canny(cropped_image, threshold1=30, threshold2=60)  

    # Find contours and filter using threshold area
    ctrs, hier = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cnts,_ = sort_contours(ctrs, x_axis_sort='LEFT_TO_RIGHT', y_axis_sort='TOP_TO_BOTTOM')
    cnts = sorted(ctrs, key=cmp_to_key(contour_sort))
    #print(len(cnts))
    ####################################
    xs =[]
    ys= []
    grid =[]

    font = cv2.FONT_HERSHEY_SIMPLEX
    cropped_grid = cropped_image.copy()
        
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ys.append(y)
        xs.append(x)
        ROI = cropped_image[y:y+h, x:x+w]
        cv2.rectangle(cropped_grid, (x, y), (x + w, y + h), (36,255,12), 2)
        
        center_x = int(ROI.shape[0]/2)
        center_y = int(ROI.shape[1]/2)
        #print(center_x,center_y)
        center_pixel = ROI[center_x][center_y]
        #print(center_pixel)
        if center_pixel>250:
            grid.append(-1)
            cv2.putText(cropped_grid,'-1', (int(x+w/2)-15,int(y+h/2)+10), font,1,(0,255,0), 1,cv2.LINE_AA)
            plt.imshow(cropped_grid)
            plt.show()
        elif center_pixel==218:
            grid.append(1)  
            cv2.putText(cropped_grid,'1', (int(x+w/2)-15,int(y+h/2)+10), font,1,(0,255,0), 1,cv2.LINE_AA)
            plt.imshow(cropped_grid)
            plt.show()
        else:
            grid.append(0)
            cv2.putText(cropped_grid,'0', (int(x+w/2)-15,int(y+h/2)+10), font,1,(0,255,0), 1,cv2.LINE_AA)
            plt.imshow(cropped_grid)
            plt.show()

    plt.imsave('edges.png',cropped_grid, cmap='gray')             
####################################################
    ys = list(np.unique(ys))
    xs = list(np.unique(xs))
    for idx, _ in enumerate(xs):
        if idx==len(xs)-1:
            break
        if (xs[idx+1]-xs[idx]) <3:
            xs.pop(idx)
    for idx, _ in enumerate(ys):
        if idx==len(ys)-1:
            break
        if (ys[idx+1]-ys[idx]) <3:
            ys.pop(idx)
###################################################
    height = len(ys)
    width = len(xs)
    print("Height:",height)
    print("Width:",width)

    

    grid= np.reshape(grid, (height, width))
    if reverse==True:
        grid[0] = grid[0][::-1]
    print(grid)
    # plt.imshow(cropped_grid, cmap='gray')
    # plt.title('findContours Image')
    # plt.show()
    
    ###################################################################################

    # Find indices of -1 using np.where()
    row_indices, col_indices = np.where(np.array(grid) == -1)
    # Combine row and column indices
    indices = list(zip(row_indices, col_indices))
    start = indices[0]
    print("start point",start)
    grid = grid.tolist()

    solution_grid = solve_one_fill(grid, start)
    
    if solution_grid:
        for row in solution_grid:
            print(row)
        for num,c in zip(flatten_comprehension(solution_grid),cnts):
            x,y,w,h = cv2.boundingRect(c)
            ROI = cropped_image[y:y+h, x:x+w]
            cv2.putText(cropped_image,str(num), (int(x+w/2),int(y+h/2)), font,1,(0,255,0), 1,cv2.LINE_AA)
 
        plt.imsave('solved.png',cropped_image,cmap='gray')  
    else:
        print("No solution found.")

#solve('img3.jpeg',reverse=False)
