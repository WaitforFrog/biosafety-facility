# BMS Communication Protocol Configuration (ModbusRTU): Setting Up RS-485 Communication Between Biosafety Equipment and Building Management System

## 适用受众
Subcontractor

## 写作角度说明
BMS通信协议配置是电气分包商将生物安全设备接入楼宇自控系统的关键工作。本模块指导分包商完成Modbus RTU通信的参数配置，包括站地址设置、通信速率、奇偶校验等，确保设备与BMS之间的正常数据交换。

## 核心论点 / 洞察
Setting all biosafety doors to the same Modbus address — a common commissioning shortcut — creates a race condition where all doors respond simultaneously, corrupting communication and generating phantom alarm floods.

## 参考素材
- Modbus RTU configuration parameters: device address (1-247, unique per device), baud rate 9600 or 19200, data bits 8, parity even (recommended) or none, stop bits 2 (even parity) or 1 (no parity)
- Communication wiring: RS-485 2-wire half-duplex, cable type Belden 3105A or equivalent, maximum daisy-chain length 1,200 m, termination resistor 120 Ω at both ends of trunk line
- Register map: Coil 00001-00020: digital outputs (door open/close, alarm reset), Register 40001-40050: analog values (differential pressure, seal pressure, cycle count)
- Read/write access: BMS typically reads all registers (polled), write access limited to control coils (00001, 00002) with password protection
- Configuration tool: handheld Modbus scanner or laptop with Modbus Poll software, test read of register 40001 (door status) as first verification step
- Troubleshooting: check TX/RX LED activity, verify polarity (+/-), confirm unique address, verify termination resistors only at cable ends

## 关键词
Modbus RTU, BMS Integration, RS-485, Communication Configuration, Register Map, Protocol Setup
