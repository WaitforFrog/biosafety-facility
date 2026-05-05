# BMS Control Point Mapping and Communication Test: Verifying Data Exchange Between Biosafety Equipment and Building Management System

## 适用受众
Commissioning_Engineer

## 写作角度说明
BMS控制点映射与通信测试是调试工程师将生物安全设备接入楼宇自控系统的核心工作。通过定义完整的控制点清单、验证通信参数配置和测试数据交换的正确性，确保BMS能够正确监控和控制设备。

## 核心论点 / 洞察
Programming BMS alarm setpoints from equipment nameplate values — without referencing the actual installed sensor calibration certificate — creates alarm setpoints that do not match the validated operating range.

## 参考素材
- Control point definition: define all input points (digital and analog) and output points with engineering units, range, update frequency, and alarm threshold
- Communication test procedure: verify Modbus polling at each register address → verify data type (float vs. integer) → verify scaling factor → verify alarm triggering at setpoint → verify acknowledgment clearing
- Modbus RTU test: use Modbus Poll or equivalent software, read all registers sequentially, verify no communication errors, record response time
- BMS integration verification: confirm BMS operator workstation displays correct values → confirm alarms trigger BMS alarm log → confirm trend logging captures data at configured interval
- Performance test: stress BMS communication with 1-second polling for 30 minutes, verify no dropped polls or data corruption

## 关键词
BMS Integration, Modbus Communication, Control Point Mapping, Communication Test, SCADA Integration, Data Exchange
