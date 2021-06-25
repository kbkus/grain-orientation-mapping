# import libraries
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None #default image size is 178956970 pixels

def correct_luminance(img):
    ''' 
    Take a 3-dimensional np.array and correct for perceptual luminance.
    Returns 2-dimensional grayscale image.
    '''
    new_img = (img[:,:,0]*0.2126) + (img[:,:,1]*0.7152) + (img[:,:,2]*0.0722)
    return new_img

def sample_img(img, width = 10000, height = 10000, inc = 10000, status = False):
    '''
    Function samples greyscale image as an array and returns dataframe with slices of
    that image
    ''' 
    if type(img) != np.ndarray:
        return print(f'Error: input image expected be a 2-dimensional np.ndarray, recieved {type(img)}.')
    
    elif len(img.shape) > 2:
        return print(f'Error: input image expected 2-dimensional array, recieved ({len(img.shape)})')
    
    else:
        # initiate empty dataframe
        df = pd.DataFrame(columns = ['slice', 'points', 'topleft'])

        width = width
        height = height
        inc = inc

        x_range = np.array([0, width])
        y_range = np.array([0, height])

        # increment for x and y to change topleft and botright values
        xinc = inc
        yinc = inc
        # number of x slices to take and number of y slices to take
        xi = img.shape[1]//inc
        yi = img.shape[0]//inc

        print(f'{yi} rows and {xi} columns to slice.')
        print(f'Total observations: {yi*xi}')
        
        # iterate through each sliding window along the height of the image
        start = time.time()
        for y in np.arange(yi):
            for x in np.arange(xi):
                
                # isolate a crop of the original images
                img_slice = img[y_range[0]:y_range[1],x_range[0]:x_range[1]]
                #print(,y_range[0], y_range[1])
                # track the top left pixel point of the slice
                topleft = (x_range[0], y_range[0])

                # put all colors into dataframe row
                df_slice = pd.DataFrame([[img_slice, [], topleft]], columns = ['slice', 'points', 'topleft'])
                #append to main dataframe
                df = df.append(df_slice, ignore_index = True)
                
                # shift sliding window to the right
                x_range += inc
                
            if status == True and y % 10 == 0:
                end = time.time()
                print(f'Runtime for row {y}/{yi} is {round(end - start,2)} seconds for {len(df)} samples')
                
            # reset sample box to left side of image
            x_range = np.array([0, width])
            # shift sample box down inc pixels
            y_range += inc
        
        return df

def plot_slice(df, n_slice=0, cmap='gray', color='red', figsize=(10,10), annotate=False):
    ''' Use dataframe that has a 'slice' column containing greyscale array of pixel values and
    'points' column containing the marked coordinates of labeled orientation pairs.
    If annotate == True, the pairs will be plotted on top of the image, if annotate=False then only the image
    will be displayed.
    color must be a color that works with plt.plot().
    cmap is the cmap of the image
    '''
    img = Image.fromarray(df['slice'][n_slice])
    plt.figure(figsize=figsize)
    plt.imshow(img, cmap=cmap)

    for pair in df['points'][n_slice]:
        plt.plot([pair[0][0], pair[1][0]],[pair[0][1], pair[1][1]], color)
    
    return 