#include <stdio.h>
#include <stdlib.h>
#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include <opencv2/opencv.hpp>   // Include OpenCV API

using namespace cv;
using namespace std;

Mat frame_to_mat(const rs2::frame& f);
Mat depth_frame_to_meters(const rs2::pipeline& pipe, const rs2::depth_frame& f);


int main(int argc, char * argv[])
{
	system("rm -fr image");
	system("rm -fr depth");
	system("mkdir image");
	system("mkdir depth");

	// Declare depth colorizer for pretty visualization of depth data
	rs2::colorizer color_map;

	rs2::config cfg1; //
	cfg1.enable_device("828112074388");
	cfg1.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
	cfg1.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);

	rs2::config cfg2; //
	cfg2.enable_device("830112070470");
	cfg2.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
	cfg2.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);

	// Declare RealSense pipeline, encapsulating the actual device and sensors
	rs2::pipeline pipe1;
	rs2::pipeline_profile selection1 = pipe1.start(cfg1);

	rs2::pipeline pipe2;
	rs2::pipeline_profile selection2 = pipe2.start(cfg2);

	auto sensor1 = selection1.get_device().first<rs2::depth_sensor>();
	auto sensor2 = selection2.get_device().first<rs2::depth_sensor>();

	auto scale1 = sensor1.get_depth_scale();
	auto scale2 = sensor2.get_depth_scale();

	cerr << "Scale-1: " << scale1 << endl;
	cerr << "Scale-2: " << scale2 << endl;

	// Camera warmup
	rs2::frameset frames1;
	rs2::frameset frames2;
	for (int i = 0; i < 30; i++) {
		frames1 = pipe1.wait_for_frames();
		frames2 = pipe2.wait_for_frames();
	}

	rs2::align align1(RS2_STREAM_COLOR);
	rs2::align align2(RS2_STREAM_COLOR);

	int cnt = 0;
	char name_c[256], name_d[256], name_e[256], name_f[256];

	while (1) {
		rs2::frameset data1 = pipe1.wait_for_frames();
		auto aligned_frames1 = align1.process(data1);   // 
		rs2::frame depth_vis1 = aligned_frames1.get_depth_frame().apply_filter(color_map);;
		rs2::frame depth1 = aligned_frames1.get_depth_frame();
		rs2::frame color1 = aligned_frames1.get_color_frame();

		rs2::frameset data2 = pipe2.wait_for_frames();
		auto aligned_frames2 = align2.process(data2);   // 
		rs2::frame depth_vis2 = aligned_frames2.get_depth_frame().apply_filter(color_map);;
		rs2::frame depth2 = aligned_frames2.get_depth_frame();
		rs2::frame color2 = aligned_frames2.get_color_frame();

		//
		auto im_c1 = frame_to_mat(color1);            //
		auto im_d1 = frame_to_mat(depth1);            //
		auto im_d_vis1 = frame_to_mat(depth_vis1);    //
		im_d1 *= 1000.0*scale1; // 

		auto im_c2 = frame_to_mat(color2);            //
		auto im_d2 = frame_to_mat(depth2);            //
		auto im_d_vis2 = frame_to_mat(depth_vis2);    //
		im_d2 *= 1000.0*scale2; // 

		// Update the window with new data
		imshow("Depth-1", im_d_vis1);
		imshow("RGB-1", im_c1);

		imshow("Depth-2", im_d_vis2);
		imshow("RGB-2", im_c2);

		waitKey(1);

		sprintf(name_c, "image/s1_color%05d.png", cnt);
		sprintf(name_d, "depth/s1_depth%05d.png", cnt);
		
		imwrite(name_c, im_c1);
		imwrite(name_d, im_d1);

		sprintf(name_e, "image/s2_color%05d.png", cnt);
		sprintf(name_f, "depth/s2_depth%05d.png", cnt);

		imwrite(name_e, im_c2);
		imwrite(name_f, im_d2);

		cerr << "Frame: " << cnt << endl;
		cnt++;
	}

	return 0;
}

// Convert rs2::frame to cv::Mat
cv::Mat frame_to_mat(const rs2::frame& f)
{
	using namespace cv;
	using namespace rs2;

	auto vf = f.as<video_frame>();
	const int w = vf.get_width();
	const int h = vf.get_height();

	if (f.get_profile().format() == RS2_FORMAT_BGR8)
	{
		//cerr<<"RS2_FORMAT_BGR8"<<endl;
		return Mat(Size(w, h), CV_8UC3, (void*)f.get_data(), Mat::AUTO_STEP);
	}
	else if (f.get_profile().format() == RS2_FORMAT_RGB8)
	{
		//cerr<<"RS2_FORMAT_RGB8"<<endl;
		auto r = Mat(Size(w, h), CV_8UC3, (void*)f.get_data(), Mat::AUTO_STEP);
		cv::cvtColor(r, r, cv::COLOR_RGB2BGR);
		return r;
	}
	else if (f.get_profile().format() == RS2_FORMAT_Z16)
	{
		//cerr<<"RS2_FORMAT_Z16"<<endl;
		return Mat(Size(w, h), CV_16UC1, (void*)f.get_data(), Mat::AUTO_STEP);
	}
	else if (f.get_profile().format() == RS2_FORMAT_Y8)
	{
		//cerr<<"RS2_FORMAT_Y8"<<endl;
		return Mat(Size(w, h), CV_8UC1, (void*)f.get_data(), Mat::AUTO_STEP);;
	}

	throw std::runtime_error("Frame format is not supported yet!");
}