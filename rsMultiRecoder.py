import pyrealsense2 as rs
import numpy as np
import cv2
import time

# Configure depth and color streams
pipeline = rs.pipeline()
pipeline2 = rs.pipeline()
pipeline3 = rs.pipeline()

config = rs.config()
config.enable_device("938422073271")	# front realsense id 938422073271
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

config2 = rs.config()
config2.enable_device("937422070270")	# left realsense id 937422070270
config2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config2.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

config3 = rs.config()
config3.enable_device("938422075202")	# left realsense id 937422070270
config3.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config3.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# right realsense id 938422075202



# Start streaming
profile = pipeline.start(config)
profile2 = pipeline2.start(config2)
profile3 = pipeline3.start(config3)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

depth_sensor2 = profile2.get_device().first_depth_sensor()
depth_scale2 = depth_sensor2.get_depth_scale()
print("Depth2 Scale is: " , depth_scale2)

depth_sensor3 = profile3.get_device().first_depth_sensor()
depth_scale3 = depth_sensor3.get_depth_scale()
print("Depth2 Scale is: " , depth_scale3)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter

clipping_distance = clipping_distance_in_meters / depth_scale
clipping_distance2 = clipping_distance_in_meters / depth_scale2
clipping_distance3 = clipping_distance_in_meters / depth_scale3

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.

align_to = rs.stream.color
align = rs.align(align_to)
align2 = rs.align(align_to)
align3 = rs.align(align_to)

imgforder_name = 'imgs_front/'
depforder_name = 'depths_front/'
imgfile_name = 'image_front'
depfile_name = 'depth_front'

imgforder_name2 = 'imgs_left/'
depforder_name2 = 'depths_left/'
imgfile_name2 = 'image_left'
depfile_name2 = 'depth_left'

imgforder_name3 = 'imgs_right/'
depforder_name3 = 'depths_right/'
imgfile_name3 = 'image_right'
depfile_name3 = 'depth_right'

file_form = '.png'

f_rgb = open('rgb_front.txt', 'w')
f_depth = open('depth_front.txt','w')

f_rgb2 = open('rgb_left.txt', 'w')
f_depth2 = open('depth_left.txt','w')

f_rgb3 = open('rgb_right.txt', 'w')
f_depth3 = open('depth_right.txt','w')

t_init = time.time()


'''
#initialize
for i in range(30):
    t1 = pipeline.wait_for_frames()
'''

print(" \'s\' key: start button")
print(" \'ctrl+c\' key: end   button")


i = 0
flag = 0

input_key = raw_input()
if input_key == 's':
	print("correct")

try:
	while True:
		i += 1
		# Wait for a coherent pair of frames: depth and color
		frames = pipeline.wait_for_frames()
		aligned_frames = align.process(frames)
		
		frames2 = pipeline2.wait_for_frames()
		aligned_frames2 = align2.process(frames2)

		frames3 = pipeline3.wait_for_frames()
		aligned_frames3 = align3.process(frames3)
		
		# get color and depth frame
		color_frame = aligned_frames.get_color_frame()
		depth_frame = aligned_frames.get_depth_frame()

		color_frame2 = aligned_frames2.get_color_frame()
		depth_frame2 = aligned_frames2.get_depth_frame()

		color_frame3 = aligned_frames3.get_color_frame()
		depth_frame3 = aligned_frames3.get_depth_frame()   
    
		#if not depth_frame or not color_frame:
		#    continue

		# Convert images to numpy arrays
		color_image = np.asanyarray(color_frame.get_data())
		depth_image = np.asanyarray(depth_frame.get_data())

		color_image2 = np.asanyarray(color_frame2.get_data())
		depth_image2 = np.asanyarray(depth_frame2.get_data())

		color_image3 = np.asanyarray(color_frame3.get_data())
		depth_image3 = np.asanyarray(depth_frame3.get_data())

		# Apply colormap on depth image (image must be converted to 8-bit per pixel first)
		depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
		depth_colormap2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image2, alpha=0.03), cv2.COLORMAP_JET)
		depth_colormap3 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image3, alpha=0.03), cv2.COLORMAP_JET)

		t = time.time()
		#depth_image = depth_image*1000.0*depth_scale 

		if flag:
			# Get data from front realsense
			cv2.imwrite(imgforder_name + imgfile_name + str(i).zfill(5) + file_form, color_image)
			cv2.imwrite(depforder_name + depfile_name + str(i).zfill(5) + file_form, depth_image)        
			f_rgb.write(str(t-t_init).zfill(16) + ' ' + imgforder_name + imgfile_name + str(i).zfill(5) + file_form  + '\n')
			f_depth.write(str(t-t_init).zfill(16) + ' ' + depforder_name + depfile_name + str(i).zfill(5) + file_form  + '\n')

			cv2.imwrite(imgforder_name2 + imgfile_name2 + str(i).zfill(5) + file_form, color_image2)
			cv2.imwrite(depforder_name2 + depfile_name2 + str(i).zfill(5) + file_form, depth_image2)        
			f_rgb2.write(str(t-t_init).zfill(16) + ' ' + imgforder_name2 + imgfile_name2 + str(i).zfill(5) + file_form  + '\n')
			f_depth2.write(str(t-t_init).zfill(16) + ' ' + depforder_name2 + depfile_name2 + str(i).zfill(5) + file_form  + '\n')

			cv2.imwrite(imgforder_name3 + imgfile_name3 + str(i).zfill(5) + file_form, color_image3)
			cv2.imwrite(depforder_name3 + depfile_name3 + str(i).zfill(5) + file_form, depth_image3)        
			f_rgb3.write(str(t-t_init).zfill(16) + ' ' + imgforder_name3 + imgfile_name3 + str(i).zfill(5) + file_form  + '\n')
			f_depth3.write(str(t-t_init).zfill(16) + ' ' + depforder_name3 + depfile_name3 + str(i).zfill(5) + file_form  + '\n')

			print((t-t_init))
		
		#print(i)
		
		if input_key == 's':
			t_init = time.time()
			flag = 1
			#i = 0
			#print('hi')
						
		elif key == 27:
			break 

		
			


finally:
    f_rgb.close()
    f_depth.close()
    f_rgb2.close()
    f_depth2.close()
    # Stop streaming
    pipeline.stop()
