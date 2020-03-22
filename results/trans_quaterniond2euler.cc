/***********************************************************************************
	> File Name: trans_quaterniond2euler.cc
	> Author: Mr Chen
	> Created Time: 2020年03月22日 星期日 11时11分06秒
	> Introduction：
 **********************************************************************************/

#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <math.h>
#include <eigen3/Eigen/Core>
#include <eigen3/Eigen/Dense>

Eigen::Vector3d Quaterniond2EulerAngle(const Eigen::Quaterniond &q) {
  Eigen::Vector3d euler;  // [roll, pitch, yaw]
  /// roll (x-axis rotation)
  double sinr_cosp = +2.0 * (q.w() * q.x() + q.y() * q.z());
  double cosr_cosp = +1.0 - 2.0 * (q.x() * q.x() + q.y() * q.y());
  euler[0] = atan2(sinr_cosp, cosr_cosp);

  /// pitch (y-axis rotation)
  double sinp = +2.0 * (q.w() * q.y() - q.z() * q.x());
  if (fabs(sinp) >= 1) {
    euler[1] = copysign(M_PI/2, sinp); // use 90 degrees if out of range
  } else {
    euler[1] = asin(sinp);
  }

  /// yaw (z-axis rotation)
  double siny_cosp = +2.0 * (q.w() * q.z() + q.x() * q.y());
  double cosy_cosp = +1.0 - 2.0 * (q.y() * q.y() + q.z() * q.z());
  euler[2] = atan2(siny_cosp, cosy_cosp);

  return euler;
}

void SaveData(std::string filename, std::map<double, Eigen::Vector3d> &time_euler) {
  std::ofstream save_data;
  save_data.open(filename.c_str());

  for (auto iter = time_euler.begin(); iter != time_euler.end(); ++iter) {
    double time = iter->first;
    Eigen::Vector3d euler = iter->second;

    save_data << time << " "
              << euler.x() << " "
              << euler.y() << " "
              << euler.z() << std::endl;
  }
}

int main() {
  std::string read_file = "./match_gt_estimate.txt";
  std::ifstream read_data;
  read_data.open(read_file.c_str());
  if (!read_data.is_open()) {
    std::cerr << "Fail to open read_file: " << read_file << std::endl;
    return -1;
  }

  double time_stamp_gt = 0.0;
  double time_stamp_estimate = 0.0;

  Eigen::Vector3d pose_gt;
  Eigen::Vector3d pose_estimate;

  Eigen::Quaterniond q_gt;
  Eigen::Quaterniond q_estimate;
  Eigen::Vector3d euler_gt;
  Eigen::Vector3d euler_estimate;
  Eigen::Vector3d diff_euler;
  std::map<double, Eigen::Vector3d> euler_gt_all;
  std::map<double, Eigen::Vector3d> euler_estimate_all;
  std::map<double, Eigen::Vector3d> diff_euler_all;

  std::string data_line;
  while (std::getline(read_data, data_line) && !data_line.empty()) {
    std::istringstream ss(data_line);
    ss >> time_stamp_gt >> pose_gt.x() >> pose_gt.y() >> pose_gt.z() >> q_gt.x() >> q_gt.y() >> q_gt.z() >> q_gt.w()
       >> time_stamp_estimate >> pose_estimate.x() >> pose_estimate.y() >> pose_estimate.z() >> q_estimate.x() >> q_estimate.y() >> q_estimate.z() >> q_estimate.w();

    euler_gt = Quaterniond2EulerAngle(q_gt);
    euler_gt =  euler_gt * 180 / M_PI;
    euler_estimate = Quaterniond2EulerAngle(q_estimate);
    euler_estimate =  euler_estimate * 180 / M_PI + Eigen::Vector3d(0, 0, 25);  // align to groundtruth
    diff_euler = euler_estimate - euler_gt;

    euler_gt_all.insert(std::make_pair(time_stamp_gt, euler_gt));
    euler_estimate_all.insert(std::make_pair(time_stamp_gt, euler_estimate));
    diff_euler_all.insert(std::make_pair(time_stamp_gt, diff_euler));
  }

  SaveData("euler_gt.txt", euler_gt_all);
  SaveData("euler_estimate.txt", euler_estimate_all);
  SaveData("euler_error.txt", diff_euler_all);

	read_data.close();
  
  return 0;
}
