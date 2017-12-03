#include <opencv2/opencv.hpp>
using namespace std;

cv::Mat frameAnalysis(cv::Mat* frame, ofstream* outputFile, char suffix);

const cv::Mat kernel = (cv::Mat_<char>(5,5) << 1, 1, 1, 1, 1,
                                  1, 1, 1, 1, 1,
                                  1, 1, 1, 1, 1,
                                  1, 1, 1, 1, 1,
                                  1, 1, 1, 1, 1);
