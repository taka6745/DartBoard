#include <iostream>
#include <opencv2/opencv.hpp>

void captureImageFromCamera() {
    cv::VideoCapture cap(0); // Open the default camera (index 0)

    if (!cap.isOpened()) {
        std::cout << "Failed to open the camera!" << std::endl;
        return;
    }

    cv::Mat frame;
    cap >> frame; // Capture a frame from the camera

    if (frame.empty()) {
        std::cout << "Failed to capture an image!" << std::endl;
        return;
    }

    // Save the captured image
    std::string filename = "captured_image.jpg";
    cv::imwrite(filename, frame);

    std::cout << "Image captured and saved as " << filename << std::endl;
}

int main() {
    captureImageFromCamera();
    return 0;
}