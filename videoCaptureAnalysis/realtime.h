#include <opencv2/opencv.hpp>
using namespace std;

cv::Mat frameAnalysis(cv::Mat* frame, ofstream* outputFile, char suffix);
double frameAnalysis_line(cv::Mat* frame, ofstream* outputFile, char suffix);

const cv::Mat kernel = cv::Mat::ones(1,1,2);
