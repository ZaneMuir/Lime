#include <opencv2/opencv.hpp>
#include <fstream>
#include <string>
#include "realtime.h"

using namespace cv;

String checkMousePos(Rect shape){
  //TODO:
  return "";
}

cv::Mat frameAnalysis(cv::Mat* frame, ofstream* outputFile, char suffix){
  Mat gray, mask, morph, demo, target;
  Rect shape=Rect(-1,-1,0,0);
  vector<vector<Point> > contours;
  vector<Vec4i> hierarchy;

  //NOTE: combine the two sub image into one!
  cvtColor(*frame, gray, COLOR_BGR2GRAY);

  inRange(gray, Scalar(0), Scalar(60),mask);//threshold
  morphologyEx(mask,morph,cv::MORPH_OPEN,kernel);
  morphologyEx(morph,morph,cv::MORPH_CLOSE,kernel);
  target = morph;
  findContours(morph, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);
  for (size_t k = 0; k<contours.size();k++){
    if (contourArea(contours[k]) > 18000){
      drawContours(target, contours, k, Scalar(150), FILLED, 8, hierarchy);
      shape = boundingRect(contours[k]);
      rectangle(target,shape,Scalar(250),2);
    }
  }
  String posLabel = checkMousePos(shape);
  *outputFile << to_string(shape.x) << "," << to_string(shape.y) << "," << to_string(shape.width) << "," << to_string(shape.height) << ","
              <<posLabel<< suffix;

  return target;
}
