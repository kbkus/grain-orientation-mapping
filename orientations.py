FRAME_HEIGHT = 800
FRAME_WIDTH = 800

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import sys
from config import df, n_slice, grid_dims, save_path

class NewFrame(tk.Frame):
    def __init__(self, row, col, count, master=None):
        self.parent = master
        self.row = row
        self.col = col
        self.count = count
        self.img = Image.fromarray(df['slice'][self.count])
        self.pts = []
        self.new_pair = []
        tk.Frame.__init__(self, self.parent, bg='green', width=FRAME_WIDTH, height=FRAME_HEIGHT)
        self.grid(row=row, column=col)
        self.canvas = self.__create_canvas()
        self.grid = self.__draw_grid(self.canvas)
        self.canvas.bind('<Button-1>', lambda event: self.getxy(self.canvas, event))
    
    def __create_canvas(self):
        width, height = self.img.size
        self.scaler = height/FRAME_HEIGHT
        canvas = tk.Canvas(self.master, bg='yellow', width=FRAME_WIDTH, height=FRAME_HEIGHT)
        canvas.grid(row=self.row, column=self.col, sticky='nesw')
        canvas.image = ImageTk.PhotoImage(self.img.resize((int(np.ceil(width/self.scaler)), FRAME_HEIGHT), Image.ANTIALIAS))
        canvas.create_image(self.row, self.col, image=canvas.image, anchor='nw')
        return canvas

    def __draw_grid(self, canvas):
        ''' Draw grid of equally spaced points on image slices for point counting.
        '''
        self.canvas = canvas
        # top left grid point x coordinate
        x0 = (FRAME_WIDTH / grid_dims[0]) / 2
        # top left grid point y coordinate
        y0 = (FRAME_HEIGHT / grid_dims[1]) / 2
        # increment to shift values for each dot
        x_inc = FRAME_WIDTH / grid_dims[0]
        y_inc = FRAME_HEIGHT / grid_dims[1]

        # create grid of cyan dots using the grid_dims parameter (rows, columns)
        for i in range(grid_dims[1]): # do left to right columns
            for j in range(grid_dims[0]): # shift down row
                self.canvas.create_oval(x0-2, y0-2, x0+2, y0+2, fill='cyan', outline='cyan')
                # increment x coordinate for plotting next point
                x0 += x_inc
            # increment y coordinate for plotting next row
            y0 += y_inc
            # reset x coordinate back to left most column
            x0 = (FRAME_WIDTH / grid_dims[0]) / 2

        # mark center of canvas with red dot
        self.canvas.create_oval((FRAME_WIDTH/2)-2, (FRAME_HEIGHT/2)-2, (FRAME_WIDTH/2)+2, (FRAME_HEIGHT/2)+2, fill='red', outline='red')

        


    def getxy(self, canvas, event):
        self.canvas = canvas
        self.new_pair.append([int(event.x*self.scaler), int(event.y*self.scaler)])
        print([int(event.x*self.scaler), int(event.y*self.scaler)])
        if len(self.new_pair) == 2:
            # add new pair to main list
            self.pts.append(self.new_pair)
            # draw line on canvas
            self.canvas.create_line(self.new_pair[0][0]/self.scaler, self.new_pair[0][1]/self.scaler, self.new_pair[1][0]/self.scaler, self.new_pair[1][1]/self.scaler, fill='red')
            # reset new_pair to be empty
            self.new_pair = []     
        self.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, fill='yellow')

    def get_pts(self):
        return self.pts


class ExportButton(tk.Frame):
    def __init__(self, count, frame1, master=None):
        self.parent = master
        self.frame1 = frame1
        self.count = count

        self.button = tk.Button(master, command=self.buttonClick, text='Export Points')
        self.button.place(x=1550, y=400)

    def buttonClick(self):
        ''' handle button click event to export all of the stored
        click coordinates'''
        print('export button clicked')
        df['points'][self.count] = self.frame1.get_pts()
        print(df['points'][0:self.count+1])
        df.to_pickle(save_path)
        

class MainWindow(tk.Frame):
    def __init__(self, count, master=None):
        self.parent = master
        self.count = n_slice
        tk.Frame.__init__(self, self.parent, bg='#ffffff')
        self.__create_layout()


    def __create_layout(self):
        self.parent.grid()
        self.Frame1 = NewFrame(0, 0, self.count, self.parent)
        self.Button = ExportButton(self.count, self.Frame1)
        self.replace_img_button = tk.Button(text='Next image', command=self.replace_img)
        self.replace_img_button.place(x=1550, y=600)

        # keep track of what image you are on
        counter = tk.Label(text='Slice #:' + str(self.count))
        counter.place(x=1550, y=650)

    def replace_img(self):
        ''' When the next image button is pressed, it will save the data 
        and change to new image.
        '''
        df['points'][self.count] = self.Frame1.get_pts()
        self.count += 1
        self.__create_layout()
        
    

def main():
    root = tk.Tk()
    
    root.title("Image Ref Window")
    root.geometry("{0}x{1}".format(2000, 2000))
    # assign cursor appearance
    root.config(cursor="draft_small")

    mw = MainWindow(20, master=root)
  
    root.mainloop()


if __name__ == '__main__':
    main()