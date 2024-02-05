#ifndef SCORECALCULATOR_HPP
#define SCORECALCULATOR_HPP

#include <vector>
#include <opencv2/core/types.hpp>

class ScoreCalculator {
public:
    int calculateScore(const std::vector<cv::Point>& dartPoints);
};

#endif
