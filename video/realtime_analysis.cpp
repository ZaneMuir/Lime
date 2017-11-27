#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

#include "realtime.h"

using namespace cv;

Rect box = Rect(-1,-1,0,0);
Rect ROILeft, ROIRight;
bool drawing = false;
bool isLeft = true;


void draw_box( Mat* img, Rect box, Scalar color = Scalar(0x00,0xff,0x00)){
    cv::rectangle(*img,
                Point(box.x,box.y),
                Point(box.x+box.width,box.y+box.height),
                color);
}

void mouse_paint_callback(int event, int x, int y, int flags, void* param){
  Mat* image = (Mat*) param;
  switch (event) {
    case EVENT_MOUSEMOVE:{
      if (drawing){
        box.width = x - box.x;
        box.height= y - box.y;
        //std::cout << "moving" << std::endl;
      }
    }
    break;

    case EVENT_LBUTTONDOWN:{
      drawing = true;
      box = Rect(x,y,0,0);
      //std::cout<< x << ", " << y << std::endl;
    }
    break;

    case EVENT_LBUTTONUP:{
      drawing = false;
      if (box.width<0){
        box.x += box.width;
        box.width *= -1;
      }
      if (box.width<0){
        box.y += box.height;
        box.height *= -1;
      }
      draw_box(image,box);
      if (isLeft){
        isLeft = false;
        ROILeft = box;
      }else{
        ROIRight = box;
      }
    }
    break;
  }
}

void roi_selector(cv::Mat* img){

  setMouseCallback("webcam_raw", mouse_paint_callback, (void*) img);
}


int main(int argc, char const *argv[]) {
  VideoCapture webcam; // create camera object.
  bool isOnline;
  if (argc != 1){
    // off-line mode
    String videoName = argv[1];
    webcam = VideoCapture(videoName);
    isOnline = false;
  } else {
    //on-line mode
    webcam = VideoCapture(0);
    isOnline = true;
  }

  std::cout << "fps: " << webcam.get(CAP_PROP_FPS) << std::endl; // print fps info.
  std::cout << "resolution: " << webcam.get(CAP_PROP_FRAME_WIDTH) << "*" << webcam.get(CAP_PROP_FRAME_HEIGHT) << std::endl; // print resolution
  if (! isOnline) std::cout << "length: " << webcam.get(CAP_PROP_FRAME_COUNT)/webcam.get(CAP_PROP_FPS) << " seconds" << std::endl; // print length
  float frameScale = 1.0;
  if (webcam.get(CAP_PROP_FRAME_WIDTH) > 720) frameScale = webcam.get(CAP_PROP_FRAME_WIDTH) / 720;
  std::cout << "scale as: " << frameScale << std::endl; // set and print scaler

  Mat frame, preview, result_left, result_right; // create image matrix.
  namedWindow("webcam_raw",WINDOW_AUTOSIZE); // create window object.

  cv::Rect target_left, target_right; // create rectangle area;
  webcam >> preview; // preview
  resize(preview, preview, Size(preview.cols/frameScale, preview.rows/frameScale));

  roi_selector(&preview);
  while (true) {
    imshow("webcam_raw",preview);
    //TODO: draw rectangle area and listen keyboard event.
    if((char)waitKey(1) == 13) break; // "ENTER" for proceeding.
  }
  ROILeft.width *= frameScale;
  ROILeft.height *= frameScale;
  ROILeft.x *= frameScale;
  ROILeft.y *= frameScale;
  ROIRight.x *= frameScale;
  ROIRight.y *= frameScale;
  ROIRight.width = ROILeft.width;
  ROIRight.height = ROILeft.height;

  namedWindow("analysis", WINDOW_OPENGL);
  //TODO: create video writer
  // realtime analysis block
  while(webcam.isOpened()){
    webcam >> frame; // nect frame.

    Mat leftFrame = frame(ROILeft);
    Mat rightFrame = frame(ROIRight);
    hconcat(leftFrame,rightFrame,preview);
    resize(preview, preview, Size(preview.cols / frameScale, preview.rows / frameScale));
    imshow("webcam_raw",preview);

    result_left = frameAnalysis(&leftFrame);
    result_right = frameAnalysis(&rightFrame);
    hconcat(result_left,result_right,preview);
    resize(preview, preview, Size(preview.cols / frameScale, preview.rows / frameScale));
    imshow("analysis",preview);

    if((char)waitKey(1) == 27) break;
  }
  return 0;
}


/*
* outline:
* 1. preview;
* 2. draw target rectangle area;
* 3. realtime analysis, including displaying and storing data.
*/
