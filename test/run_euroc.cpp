#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <thread>
#include <iomanip>

#include <cv.h>
#include <opencv2/opencv.hpp>
#include <highgui.h>
#include <eigen3/Eigen/Dense>
#include "System.h"

using namespace std;
using namespace cv;
using namespace Eigen;

const int nDelayTimes = 2;
std::string sData_path;
std::string sConfig_path;

std::shared_ptr<System> pSystem;

void PubImuData() {
	string sImu_data_file = sData_path + "imu0/data.csv";
	cout << "1 PubImuData start sImu_data_filea: " << sImu_data_file << endl;
	ifstream fsImu;
	fsImu.open(sImu_data_file.c_str());
	if (!fsImu.is_open()) {
		cerr << "Failed to open imu file! " << sImu_data_file << endl;
		return;
	}

	std::string sImu_line;
	double dStampNSec = 0.0;
	Vector3d vAcc;
	Vector3d vGyr;
  char tmp;
  bool skip_first_line = true;
  /// read imu data
	while (std::getline(fsImu, sImu_line) && !sImu_line.empty()) {
    if (skip_first_line) {
      skip_first_line = false;
      continue;
    }
		std::istringstream ssImuData(sImu_line);
		ssImuData >> dStampNSec >> tmp >> vGyr.x() >> tmp >> vGyr.y() >> tmp >> vGyr.z() >> tmp 
              >> vAcc.x() >> tmp >> vAcc.y() >> tmp >> vAcc.z();
		// cout << "Imu t: " << fixed << dStampNSec << " gyr: " << vGyr.transpose() << " acc: " << vAcc.transpose() << endl;
		pSystem->PubImuData(dStampNSec/1e9, vGyr, vAcc);
		usleep(5000*nDelayTimes);
	}
	fsImu.close();
}

void PubImageData() {
	string sImage_file = sData_path + "cam0/data.csv";
	cout << "1 PubImageData start sImage_file: " << sImage_file << endl;
	ifstream fsImage;
	fsImage.open(sImage_file.c_str());
	if (!fsImage.is_open()) {
		cerr << "Failed to open image file! " << sImage_file << endl;
		return;
	}

	std::string sImage_line;
	double dStampNSec;
	string sImgFileName;
  char tmp;
  bool skip_first_line = true;
	// cv::namedWindow("SOURCE IMAGE", CV_WINDOW_AUTOSIZE);
	while (std::getline(fsImage, sImage_line) && !sImage_line.empty()) {
    if (skip_first_line) {
      skip_first_line = false;
      continue;
    }
		std::istringstream ssImuData(sImage_line);
		ssImuData >> dStampNSec >> tmp >> sImgFileName;
		// cout << "Image t : " << fixed << dStampNSec << " Name: " << sImgFileName << endl;
		string imagePath = sData_path + "cam0/data/" + sImgFileName;
		Mat img = imread(imagePath.c_str(), 0);
		if (img.empty()) {
			cerr << "image is empty! path: " << imagePath << endl;
			return;
		}
		pSystem->PubImageData(dStampNSec/1e9, img);
		// cv::imshow("SOURCE IMAGE", img);
		// cv::waitKey(0);
		usleep(50000*nDelayTimes);
	}
	fsImage.close();
}

int main(int argc, char **argv) {
	if (argc != 3) {
	  cerr << "cmd: ./run_euroc PATH_TO_FOLDER/euroc_data/ PATH_TO_CONFIG/config/\n"
		  	 << "For example: ./run_euroc ../euroc_data/MH_03_medium/ ../config/" << endl;
		return -1;
	}

	sData_path = argv[1];    // "../euroc_data/MH_05_difficult/"
	sConfig_path = argv[2];  // "../config/"

	pSystem.reset(new System(sConfig_path));

	std::thread thd_BackEnd(&System::ProcessBackEnd, pSystem);
	// sleep(5);
	std::thread thd_PubImuData(PubImuData);
	std::thread thd_PubImageData(PubImageData);
	std::thread thd_Draw(&System::Draw, pSystem);

	thd_PubImuData.join();
	thd_PubImageData.join();
	thd_BackEnd.join();
	thd_Draw.join();
	cout << "main end... see you ..." << endl;

	return 0;
}
