#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>

#include <iostream>
//#include <sstream>  //string to number
//#include <string>   //strings
//#include <iomanip>  //controlling float print precision

using namespace cv;

int main(int argc, char const *argv[]) {

  VideoCapture webcam = VideoCapture(0); // front webcam
  Mat frame;
  namedWindow("webcam",WINDOW_AUTOSIZE);

  std::cout << "fps: "<<webcam.get(CAP_PROP_FPS) << std::endl;

  while(webcam.isOpened()){
    webcam >> frame;
    imshow("webcam",frame);
    if((char)waitKey(1) == 27) break;
  }
  return 0;
}
