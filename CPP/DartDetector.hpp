#ifndef DARTDETECTOR_HPP
#define DARTDETECTOR_HPP

#include <opencv2/core/mat.hpp>
#include <vector>

class DartDetector {
public:
    std::vector<cv::Point> detect(const cv::Mat& frame);
};

#endif
