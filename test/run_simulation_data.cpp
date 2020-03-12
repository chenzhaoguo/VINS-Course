#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <thread>
#include <iomanip>

#include <cv.h>
#include <opencv2/opencv.hpp>
#include <highgui.h>
#include <eigen3/Eigen/Dense>
#include "System.h"

using namespace cv;
using namespace Eigen;

const int nDelayTimes = 2;
std::string sData_path;
std::string sConfig_path;

std::shared_ptr<System> pSystem;

void PubImuData() {
  std::string imu_data_file = sData_path + "imu_pose_noise.txt";
	std::cout << "1 PubImuData imu_data_file: " << imu_data_file << std::endl;
  std::ifstream read_imu;
  read_imu.open(imu_data_file.c_str());
  if (!read_imu.is_open()) {
    std::cerr << "Fail to open imu_data_file: " << imu_data_file << std::endl;
    return;
  }

  std::string imu_data_line;
  double stamp_ns = 0.0;
  Eigen::Quaterniond Qwb;
  Eigen::Vector3d position_twb;
  Eigen::Vector3d gyro_data;
  Eigen::Vector3d acc_data;
  /// read imu data
  while (std::getline(read_imu, imu_data_line) && !imu_data_line.empty()) {
    std::istringstream ss(imu_data_line);
    ss >> stamp_ns >> Qwb.w() >> Qwb.x() >> Qwb.y() >> Qwb.z() >> position_twb.x() >> position_twb.y() >> position_twb.z()
       >> gyro_data.x() >> gyro_data.y() >> gyro_data.z()
       >> acc_data.x() >> acc_data.y() >> acc_data.z();
		pSystem->PubImuData(stamp_ns, gyro_data, acc_data);
		usleep(5000*nDelayTimes);
  }
	read_imu.close();
}

void PubImageData() {
  std::string cam_pose_file = sData_path + "cam_pose_tum.txt";  // 给目录keyframe/中每一帧相机观测到的路标点的数据文件提供时间戳
	std::cout << "2 PubImageData cam_pose_file: " << cam_pose_file << std::endl;
  std::ifstream read_cam_pose;
  read_cam_pose.open(cam_pose_file.c_str());
  if (!read_cam_pose.is_open()) {
    std::cerr << "Fail to open cam_pose_file: " << cam_pose_file << std::endl;
    return;
  }

  std::string cam_pose_line;
  double stamp_ns = 0.0;
  int points_file_id = 0;  // 用于索引不同帧相机所观测到的特征点的文件
  /// read timestamp from cam_pose_tum.txt && read points from keyframe/
  while (std::getline(read_cam_pose, cam_pose_line) && !cam_pose_line.empty()) {
    std::vector<Eigen::Vector2d> feature_point;  // 当前帧相机观测到的路标点在归一化平面上的相机坐标
    std::istringstream ss(cam_pose_line);
    ss >> stamp_ns;

    std::stringstream points_file_corresponding;
    points_file_corresponding << "keyframe/all_points_" << points_file_id << ".txt";
    std::string points_file = sData_path + points_file_corresponding.str();
    points_file_id++;
    std::ifstream read_points;
    read_points.open(points_file.c_str());
    if (!read_points.is_open()) {
      std::cerr << "Fail to open points_file: " << points_file << std::endl;
      return;
    }

    std::string points_line;
    while (std::getline(read_points, points_line) && !points_line.empty()) {
      Eigen::Vector4d point_w;
      Eigen::Vector2d feature_c;
      std::stringstream ss(points_line);
      ss >> point_w[0] >> point_w[1] >> point_w[2] >> point_w[3]
         >> feature_c.x() >> feature_c.y();
      feature_point.push_back(feature_c);
    }
		pSystem->PubImageData(stamp_ns, feature_point);
		usleep(50000*nDelayTimes);
    read_points.close();
  }
	read_cam_pose.close();
}

int main(int argc, char **argv) {
	if (argc != 3) {
	  std::cerr << "cmd: ./run_simulation PATH_TO_FOLDER/ PATH_TO_CONFIG/\n"
		  	      << "For example: ./run_simulation ../simulation_data/ ../config/" << std::endl;
		return -1;
	}

	sData_path = argv[1];    // "../simulation_data/"
	sConfig_path = argv[2];  // "../config/"

	pSystem.reset(new System(sConfig_path));

	std::thread thd_BackEnd(&System::ProcessBackEnd, pSystem);
	// sleep(5);
	std::thread thd_PubImuData(PubImuData);
	std::thread thd_PubImageData(PubImageData);
	// std::thread thd_Draw(&System::Draw, pSystem);

	thd_PubImuData.join();
	thd_PubImageData.join();
	thd_BackEnd.join();
	// thd_Draw.join();
	std::cout << "...main() end..." << std::endl;

	return 0;
}
