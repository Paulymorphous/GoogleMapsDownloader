# Download Images from Google Maps

You can use this script to download iamges from Google Maps. You will recieve the output in form of 256x256 tiles, along with the coordinate of each image.

## Requirements
Make sure that you have the following libraries installed:
1. PIL
2. Matplotlib

## Running the script
You can run the script using the following command:

**python GoogleMapDownloader.py --lat 54.34676 --lng 64.46675 --zoom 20 --batch A1 --num 20**

Arguments:
1. --lat - Latitude of the target location.
2. --lng - Longitude of the target location.
3. --zoom - Zoom level of the output Images. Default value is 20.
4. --batch - If you want to download images in batches, then use this to set the batch id.
5. --num - The number of images you want to download. Default value is 10.

**WARNING:** Usng this script to download images is not recommended as Google will block your IP for a period of 24 hours if you pull more than a certain numebr of imgages. This means that you will have trouble accessing Google Maps thereafter. Therefore, I recommend that you use a VPN and keep switching countries for evey batch.

