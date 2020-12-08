# RealSense-Example

Example of realsense libraires (C++ , Python)  

I test this code with **Real Sense d435**.  

- `realsenseVisualize.cpp`
  - Input : One real sense d435 camera  
  - Output : OpenCV windows (RGB Image and Depth Image)  
  - See RGB image and depth image with align. (Depth image is align to RGB image)  
  
- `rs-imshow.cpp`
  - Input : Two real sense d435 cameras, The folder should be ready.  
  - Output : 4 Folders for sequence Images (One camera has 2 outputs. One is for RGB, the other is for Depth)  
  - Save the RGB Image and Depth Image with 2 real sense cameras.  

- `rsMultiRecoder.py`  
  - Input : Three real sense d435 cameras  
  - Output :  
    6 Folder for sequence Images (One camera has 2 outputs. One is for RGB, the other is for Depth) - Folders are  
    3 TimeStamp.txt (Each real sense Camera)  
