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
#include <eigen3/Eigen/Geometry>

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

/// InputFile(Tum file): timestamp px py pz qx qy qz qw.  OutputFile: timestamp roll pitch yaw
void TumQuat2Euler(std::string filename, std::map<double, Eigen::Vector3d> &time_euler) {
  std::ifstream read_data;
  read_data.open(filename.c_str());
  if (!read_data.is_open()) {
    std::cerr << "Fail to open read_file: " << filename << std::endl;
    return;
  }

  long double time_stamp = 0.0;
  Eigen::Vector3d pose;
  Eigen::Quaterniond q;
  Eigen::Vector3d euler;

  std::string data_line;
  while (std::getline(read_data, data_line) && !data_line.empty()) {
    std::istringstream ss(data_line);
    ss >> time_stamp >> pose.x() >> pose.y() >> pose.z() >> q.x() >> q.y() >> q.z() >> q.w();

    euler = Quaterniond2EulerAngle(q);
    // euler = q.toRotationMatrix().eulerAngles(2,1,0);
    euler =  euler * 180 / M_PI;
    time_euler.insert(std::make_pair(time_stamp, euler));
  }
	read_data.close();
}

void CalEulerErr(std::string filename, std::map<double, Eigen::Vector3d> &diff_euler_all) {
  std::ifstream read_data;
  read_data.open(filename.c_str());
  if (!read_data.is_open()) {
    std::cerr << "Fail to open read_file: " << filename << std::endl;
    return;
  }

  long double time_stamp_gt = 0.0;
  long double time_stamp_estimate = 0.0;

  Eigen::Vector3d pose_gt;
  Eigen::Vector3d pose_estimate;

  Eigen::Quaterniond q_gt;
  Eigen::Quaterniond q_estimate;
  Eigen::Vector3d euler_gt;
  Eigen::Vector3d euler_estimate;
  Eigen::Vector3d diff_euler;

  std::string data_line;
  while (std::getline(read_data, data_line) && !data_line.empty()) {
    std::istringstream ss(data_line);
    ss >> time_stamp_gt >> pose_gt.x() >> pose_gt.y() >> pose_gt.z() >> q_gt.x() >> q_gt.y() >> q_gt.z() >> q_gt.w()
       >> time_stamp_estimate >> pose_estimate.x() >> pose_estimate.y() >> pose_estimate.z() >> q_estimate.x() >> q_estimate.y() >> q_estimate.z() >> q_estimate.w();

    euler_gt = Quaterniond2EulerAngle(q_gt);
    // euler_gt = q_gt.toRotationMatrix().eulerAngles(2,1,0);
    euler_gt =  euler_gt * 180 / M_PI;
    euler_estimate = Quaterniond2EulerAngle(q_estimate);
    // euler_estimate = q_estimate.toRotationMatrix().eulerAngles(2,1,0);
    euler_estimate =  euler_estimate * 180 / M_PI + Eigen::Vector3d(0, 0, 27.5);  // align to groundtruth
    diff_euler = euler_estimate - euler_gt;
    diff_euler_all.insert(std::make_pair(time_stamp_gt, diff_euler));
  }
	read_data.close();
}

int main() {
  /// groundtruth_MH_04.tum最后4列的四元数转换为欧拉角
  std::string gt_file = "./groundtruth_V1_01.tum";
  std::map<double, Eigen::Vector3d> euler_gt_all;
  TumQuat2Euler(gt_file, euler_gt_all);
  SaveData("euler_gt.txt", euler_gt_all);

  std::string est_file = "./estimate_result.txt";
  std::map<double, Eigen::Vector3d> euler_est_all;
  TumQuat2Euler(est_file, euler_est_all);
  for (auto iter = euler_est_all.begin(); iter != euler_est_all.end(); ++iter) {
    // Eigen::Vector3d euler = iter->second;
    iter->second += Eigen::Vector3d(0, 0, 26);
  }
  SaveData("euler_estimate.txt", euler_est_all);
  
  /// 计算aligned后的欧拉角误差
  std::string match_file = "./match_gt_estimate.txt";
  std::map<double, Eigen::Vector3d> diff_euler_all;
  CalEulerErr(match_file, diff_euler_all);
  SaveData("euler_error.txt", diff_euler_all);

  return 0;
}
