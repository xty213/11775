#include <stdio.h>
#include <iostream>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"


int main(int argc, const char* argv[])
{
    // read the gray scale input image
    const cv::Mat input = cv::imread(argv[1], 0);

    // get the keypoints
    cv::SiftFeatureDetector detector;
    std::vector<cv::KeyPoint> keypoints;
    detector.detect(input, keypoints);

    // compute descriptors
    cv::Mat output;
    cv::DescriptorExtractor::create("SIFT")->compute(input, keypoints, output);
    std::cout << output << std::endl;

    return 0;
}
