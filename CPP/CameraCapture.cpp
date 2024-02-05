#include "CameraCapture.hpp"

CameraCapture::CameraCapture() : cap(0) { // Default camera
    if (!cap.isOpened()) {
        throw std::runtime_error("Failed to open camera");
    }
}

cv::Mat CameraCapture::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}
