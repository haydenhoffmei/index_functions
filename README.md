# Index Functions
### Description
Python script to execute remote sensing indices on GeoTIFF images.
### Current Capacity
The script currently works contains the NDVI, EVI (two band), SAVI, and GCI indices which are primarily used for vegetation detection.  It is also setup to read in the blue, green, red, and near infrared bands. Both the band number and indices are highly modular, and can be expanded to incorporate more options based on user needs. 

The current script is setup up to loop through an initial directory, with subdirectories containing scenes, divided by band. This can be tweaked to read each band independently from a single composite GeoTIFF if necessary.
### Dependencies
The script uses rasterio and numpy (current scrip also uses matplotlib to show results, but this is optional).
