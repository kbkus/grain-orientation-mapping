# import dependencies
import pandas as pd
from PIL import Image


# define dataframe and load file
df = pd.read_pickle('orientations.pkl')

# slice to start marking orientations on
n_slice = 6

# save file 
save_path = 'orientations.pkl'

# dimensions for point counting grid (row, col)
grid_dims = (5, 5)