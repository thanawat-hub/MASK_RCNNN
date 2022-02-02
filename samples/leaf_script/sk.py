
from skimage import io

# Create a list to store the urls of the images
urls = ["https://iiif.lib.ncsu.edu/iiif/0052574/full/800,/0/default.jpg",
       "https://iiif.lib.ncsu.edu/iiif/0016007/full/800,/0/default.jpg",
      "https://placekitten.com/800/571"]  
# Read and display the image
# loop over the image URLs, you could store several image urls in the list

# image = io.imread(urls[0])
filename = "C:\Users\User PC\Downloads\type1_B100.png"
image = io.imread(filename)
print(image.shape)