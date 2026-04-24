# BMS Communication Protocol Configuration (ModbusTCP): Setting Up TCP/IP Ethernet Communication Between Biosafety Equipment and Building Management System

## 适用受众
Subcontractor

## 写作角度说明
ModbusTCP是电气分包商将生物安全设备通过以太网接入BMS系统的通信协议配置工作。相比Modbus RTU，ModbusTCP具有更高的通信速率和更长的通信距离，适合大型设施的多设备集中管理。

## 核心论点 / 洞察
Connecting biosafety equipment to the same Ethernet network segment as office IT systems — without network isolation via VLAN — exposes the equipment's ModbusTCP interface to network security risks and traffic congestion that degrades communication reliability.

## 参考素材
- ModbusTCP configuration: device IP address (static IP required, default typically 192.168.1.100) → subnet mask → default gateway → Modbus unit ID (1-247, same as RTU)
- Network isolation: configure dedicated VLAN for building automation systems → separate from corporate IT network → configure firewall rules to allow only BMS server access to equipment IP addresses
- Communication parameters: TCP port 502 (standard Modbus port) → connection timeout (recommended 3 seconds) → retry count (recommended 3) → polling interval (500 ms minimum for ModbusTCP)
- Register mapping: ModbusTCP uses same register addressing as Modbus RTU (40001-49999 for holding registers, 10001-19999 for input registers) → function codes 03 (read holding), 04 (read input), 06 (write single), 16 (write multiple)
- Troubleshooting: verify IP connectivity with ping → verify port 502 is listening with telnet → check for IP address conflict → verify no duplicate Modbus unit IDs on the network

## 关键词
Modbus TCP, BMS Ethernet, Network Configuration, VLAN, IP Address, Protocol Setup
