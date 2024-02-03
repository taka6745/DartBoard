### README.md - DartScoreTracker: A C++ Application for Recording Dart Scores in Cricket

#### Overview

DartScoreTracker is an ongoing collaborative project developed by myself and a friend from computer science. Our goal is to create a robust C++ application that leverages image processing techniques to automatically record scores in the game of Cricket played on a dartboard. This project aims to bridge the gap between traditional dart scoring methods and modern technology, providing a seamless and automated way to track scores, enhance accuracy, and improve the overall gaming experience.

#### How It Works

The application utilizes a camera to continuously monitor a dartboard. Through advanced image processing algorithms, it detects darts' positions on the board after each throw and calculates the corresponding scores based on Cricket rules. The scores are then displayed in real-time, providing players with instant feedback on their performance.

#### System Setup

- **Camera Setup**: A high-definition camera is mounted with a clear view of the dartboard. It should be positioned to minimize occlusions and ensure consistent lighting for accurate dart detection.
- **Software Requirements**: The application is built using C++ with OpenCV for image processing. Users will need to install OpenCV and compile the application from source.
- **Running the Application**: After compiling, the application can be started before beginning a game of Cricket. The camera feed is analyzed in real-time, with scores updated after each throw.

#### Project Structure

- `main.cpp`: The entry point of the application, orchestrating the camera feed processing and score calculation.
- `DartDetector.hpp/cpp`: Contains logic for detecting darts on the dartboard using image processing.
- `ScoreCalculator.hpp/cpp`: Responsible for calculating scores based on detected dart positions.
- `CameraCapture.hpp/cpp`: Manages camera initialization and frame capture.

#### To-Do List

- [ ] Implement the camera feed capture module.
- [ ] Develop the dart detection algorithm.
- [ ] Create the score calculation logic based on Cricket rules.
- [ ] Design a user interface to display real-time scores and game statistics.
- [ ] Test the application in various lighting and setup conditions to ensure reliability.
- [ ] Optimize performance for real-time processing.

#### Expected Performance and Limitations

The application aims to achieve high accuracy in dart detection and score calculation under optimal conditions. However, performance may vary based on several factors such as lighting, camera quality, and dartboard visibility. Further testing and optimization will be conducted to address these challenges.

#### Contribution

This project is open to contributions. We welcome suggestions, improvements, and bug fixes. Please feel free to fork the repository, make changes, and submit pull requests.

#### License

This project is licensed under the MIT License - see the LICENSE file for details.
