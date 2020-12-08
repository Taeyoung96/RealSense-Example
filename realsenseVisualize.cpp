#include <iostream>
#include <librealsense2/rs.hpp> 
#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

// Visualize Depth Image(with out Colorization) and RGB Image using OpenCV

int main(){
    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    rs2::config cfg;

    cfg.enable_stream(RS2_STREAM_DEPTH);
    cfg.enable_stream(RS2_STREAM_COLOR);

    // Start streaming with default recommended configuration
    pipe.start();

    // Defbine two align objects. One will be used to align
    // to depth viewport and the other to color.
    // Creating align oject is an expensive operation
    // that should not be performed in the main loop
    rs2::align align_to_color(RS2_STREAM_COLOR);

    // Declare Window name
    const auto window_name = "Display Depth";
    namedWindow(window_name,CV_WINDOW_AUTOSIZE);

    while (true)
    {
        rs2::frameset data = pipe.wait_for_frames(); // Wait for next set of frames from the camera
        auto aligned_frames = align_to_color.process(data); // align to depth viewpoint with color image

        // Get Depth and Color frame
        rs2::depth_frame depth = aligned_frames.get_depth_frame();
        rs2::frame color = aligned_frames.get_color_frame();

        // Declare width and height
        const int w_depth = depth.get_width();
        const int h_depth = depth.get_height();

        const int w_img = color.as<rs2::video_frame>().get_width();
        const int h_img = color.as<rs2::video_frame>().get_height();

        // Create OpenCV matrix of size (w,h) from the colorized depth data
        Mat imageDepth(Size(w_depth, h_depth), CV_16UC1, (void*)depth.get_data(), Mat::AUTO_STEP);
        // Create OpenCV matrix of size (w,h) from the RGB image data
        Mat imageRGB(Size(w_img, h_img), CV_8UC3, (void*)color.get_data(), Mat::AUTO_STEP);

        cv::cvtColor(imageRGB,imageRGB,CV_BGR2RGB); // Convert BGR to RGB
        
        // Update the window with new depth data
        imshow(window_name, imageDepth);
        // Update the window and show RGB Image
        imshow("frame",imageRGB);
    }

    return 0;
}