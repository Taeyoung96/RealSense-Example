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

# Start streaming
profile = pipeline.start(config)  # front
profile2 = pipeline2.start(config2)   # left
profile3 = pipeline3.start(config3)   # right	

profile = pipeline.get_active_profile()
profile2 = pipeline2.get_active_profile()
profile3 = pipeline3.get_active_profile()
#print(profile)

# Get video stream
color_profile_f = rs.video_stream_profile(profile.get_stream(rs.stream.color))
depth_profile_f = rs.video_stream_profile(profile.get_stream(rs.stream.depth))

color_profile_l = rs.video_stream_profile(profile2.get_stream(rs.stream.color))
depth_profile_l = rs.video_stream_profile(profile2.get_stream(rs.stream.depth))

color_profile_r = rs.video_stream_profile(profile3.get_stream(rs.stream.color))
depth_profile_r = rs.video_stream_profile(profile3.get_stream(rs.stream.depth))

# Get front camera intrinsics
depth_intrinsics_front = depth_profile_f.get_intrinsics()
color_intrinsics_front = color_profile_f.get_intrinsics()
print("front color instrinscics")
print(color_intrinsics_front)
print("--------------------------------------------")
print("front depth instrinscics")
print(depth_intrinsics_front)

# Get left camera intrinsics
depth_intrinsics_left = depth_profile_l.get_intrinsics()
color_intrinsics_left = color_profile_l.get_intrinsics()
print("left color instrinscics")
print(color_intrinsics_left)
print("--------------------------------------------")
print("left depth instrinscics")
print(depth_intrinsics_left)

# Get right camera intrinsics
depth_intrinsics_right = depth_profile_r.get_intrinsics()
color_intrinsics_right = color_profile_r.get_intrinsics()
print("right color instrinscics")
print(color_intrinsics_right)
print("--------------------------------------------")
print("right depth instrinscics")
print(depth_intrinsics_right)

# Stop streaming
pipeline.stop()
pipeline2.stop()
pipeline3.stop()

