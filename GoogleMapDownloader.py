import urllib.request
from PIL import Image
from matplotlib import pyplot as plt
import os
import math
import argparse
import pickle

IMAGE_SIZE = 256
OUTPUT_FOLDER = "Images/"

def get_XY(_lat, _lng, _zoom):
      
        tile_size = IMAGE_SIZE
        numTiles = 1 << _zoom
        point_x = (tile_size/ 2 + _lng * tile_size / 360.0) * numTiles // tile_size
        sin_y = math.sin(_lat * (math.pi / 180.0))
        point_y = ((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size
        return int(point_x), int(point_y)
        
def generate_images(_lat, _lng, _zoom, id, batch):
        
      
        tile_width = 1
        tile_height = 1

        start_x, start_y = get_XY(_lat, _lng, _zoom)
        
        width, height = IMAGE_SIZE * tile_width, IMAGE_SIZE * tile_height
       
        for x in range(0, tile_width):
            for y in range(0, tile_height) :
             
                map_img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE))
      
                url = 'https://mt0.google.com/vt/lyrs=s&?x=' + str(start_x+x)+'&y='+str(start_y+y)+'&z='+str(_zoom)
                current_tile = str(x)+'-'+str(y)
                urllib.request.urlretrieve(url, current_tile)
            
                im = Image.open(current_tile)
                map_img.paste(im)
                filename = batch + '_'+ str(id) + ".png"
                map_img.save(OUTPUT_FOLDER+filename)
                os.remove(current_tile)
        
        return filename
        
def get_point_lat_lng(lat, lng, zoom, w, h, x, y):
    parallelMultiplier = math.cos(lat * math.pi / 180)
    degreesPerPixelX = 360 / math.pow(2, zoom + 8)
    degreesPerPixelY = 360 / math.pow(2, zoom + 8) * parallelMultiplier
    pointLat = lat - degreesPerPixelY * ( y - h / 2)
    pointLng = lng + degreesPerPixelX * ( x - w / 2)

    return (pointLat, pointLng)

def main():
    
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--lat', help = 'Latitude of the location.')
    parser.add_argument('--lng', help = 'Longitude of the location.')
    parser.add_argument('--zoom', help = 'Desired zoom level.', default =20)
    parser.add_argument('--batch',help = 'Batch id.', default = "1")
    parser.add_argument('--num', help = 'Number of Images', default = 10)
    
    args = parser.parse_args()  
  
    lat = float(args.lat)
    lng = float(args.lng)
    zoom = int(args.zoom)
  
    cords = get_XY(lat, lng, zoom)
    print("The tile coordinates are {}, {}".format(cords[0],cords[1]))
    
  
    try:
        with open(OUTPUT_FOLDER+"BATCH_"+args.batch+'_coordinates.txt', 'w') as file:
            data = "Filename, Latitude, Longitude" + "\n"
            file.write(data)
            id = 0
            for x in range(0, int(math.sqrt(int(args.num)))):
                for y in range(0, int(math.sqrt(int(args.num)))):
                    id += 1
                    _lat = lat + 0.001 * x
                    _lng = lng + 0.001 * y
                    filename = generate_images(_lat, _lng, zoom, id, args.batch)
                    #_lat, _lng = get_point_lat_lng(_lat, _lng, zoom, 256, 256, -256/2, 256/2)
                    data = filename + ',' + str(_lat)+','+str(_lng)+'\n'
             
                    file.write(data)
            
    except IOError as e:
        print(e)
        
    else:
        print("The map has successfully been created")


if __name__ == '__main__':  
    main()

