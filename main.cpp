#include "CameraCapture.hpp"
#include "DartDetector.hpp"
#include "ScoreCalculator.hpp"
#include <opencv2/opencv.hpp>

int main() {
    CameraCapture camera;
    DartDetector dartDetector;
    ScoreCalculator scoreCalculator;

    cv::Mat frame;
    while (true) {
        frame = camera.getFrame();
        if (frame.empty()) break;

        std::vector<cv::Point> dartPoints = dartDetector.detect(frame);
        int score = scoreCalculator.calculateScore(dartPoints);

        // Optional: Display the processed frame with detections and score
        // cv::imshow("Dart Score Recorder", frame);

        if (cv::waitKey(30) >= 0) break;
    }

    return 0;
}
