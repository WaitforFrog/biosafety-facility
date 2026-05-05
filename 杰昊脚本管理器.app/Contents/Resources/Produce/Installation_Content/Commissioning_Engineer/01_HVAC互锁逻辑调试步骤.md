# HVAC Interlock Logic Debugging: Verifying Fan, Damper, and Pressure Control Sequence Operation

## 适用受众
Commissioning_Engineer

## 写作角度说明
HVAC互锁逻辑的调试是确保生物安全设备与建筑通风系统正确联动的关键步骤。调试工程师需要验证送排风系统的时序逻辑、压差控制精度和紧急情况下的安全联锁功能，确保设备在各种运行工况下都能维持正确的压力梯度。

## 核心论点 / 洞察
In biosafety containment systems, the most frequent commissioning failure is incorrect HVAC interlock sequencing — fans starting before dampers open creates transient negative pressure that compromises containment integrity.

## 参考素材
- Interlock sequence verification: exhaust fan start → return air damper open (0-10V, 3-second delay) → supply fan start → supply air damper open → pressure setpoint achieved (10-15 Pa over adjacent zone)
- BMS communication protocol: Modbus RTU (RS-485, 9600 baud, even parity) or Modbus TCP (Ethernet), polling interval ≤500 ms
- Pressure control tuning: PID parameters for differential pressure control (typical: P=0.5, I=10s, D=0s), response time target <30 seconds to reach setpoint
- Emergency shutdown sequence: door open signal → 5-second delay → supply fan to minimum speed → exhaust damper close to 20% → alarm activation
- Test procedure: witnessed test of each interlock condition under simulated fault conditions, documented in commissioning log

## 关键词
HVAC Interlock, Damper Sequence, Pressure Control, BMS Integration, Commissioning Test, PID Tuning
