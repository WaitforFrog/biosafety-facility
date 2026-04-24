# HVAC Airflow Volume and Differential Pressure Control Point Configuration: Setting Up BMS Data Points for Air Handling Integration

## 适用受众
Subcontractor

## 写作角度说明
HVAC风量与压差控制点配置是HVAC分包商将生物安全设备的风量传感器和压差控制点接入BMS系统的关键配置工作。本模块定义需要配置的数据点类型、控制策略和与设备控制器的接口参数。

## 核心论点 / 洞察
Configuring the pressure differential setpoint based on the BMS operator's preferred value — without verifying the value against the equipment's validated operating range from the commissioning report — risks operating outside the validated containment envelope.

## 参考素材
- Control point list: supply air flow rate (m³/h or CFM) → exhaust air flow rate (m³/h or CFM) → differential pressure setpoint (Pa) → differential pressure measured value (Pa) → alarm setpoint (Pa) → outdoor air damper position (%)
- Control strategy: cascade control (pressure PID loop controls supply fan speed, exhaust fan tracks supply) → lead-lag control (exhaust fan leads, supply follows) → static pressure reset (reduce setpoint when zone is unoccupied)
- BMS integration points: each control point must have Modbus register address → data type (integer or float) → scaling factor (e.g., register value of 100 = 10.0 Pa) → engineering unit → update rate
- Commissioning data points: additional points for commissioning use (may be read-only for BMS operator): seal inflation pressure (bar) → door cycle count → alarm log pointer → sensor calibration date
- Performance monitoring: configure BMS trend logs for all key parameters → set up daily data archiving → establish alarm thresholds for out-of-range values

## 关键词
HVAC Integration, Pressure Control, Airflow Setpoint, BMS Configuration, PID Control, Building Automation
