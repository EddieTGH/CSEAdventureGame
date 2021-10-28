from PIL import Image
import os.path
import matplotlib.pyplot as plt

#print("Height = ", len(plt.imread('src/RESIZED_laundry_key.png').copy()), "\tWidth = ", len(plt.imread('src/RESIZED_laundry_key.png')[0]))



im1 = Image.open('src/HARP.png').resize((24, 30))
directory = os.getcwd() # Use working directory if unspecified
src_directory = os.path.join(directory, "backpackIconFiles\\")
filename = os.path.join(src_directory, "harp.png")
im1.save(filename, 'png')
