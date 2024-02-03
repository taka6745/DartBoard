#ifndef CAMERACAPTURE_HPP
#define CAMERACAPTURE_HPP

#include <opencv2/videoio.hpp>

class CameraCapture {
    cv::VideoCapture cap;

public:
    CameraCapture();
    cv::Mat getFrame();
};

#endif
