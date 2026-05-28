#!/bin/bash

BASE="cowrie/honeyfs"

mkdir -p "$BASE/etc"
mkdir -p "$BASE/var/log"
mkdir -p "$BASE/opt/meddevice"
mkdir -p "$BASE/proc"
mkdir -p "$BASE/tmp"
mkdir -p "$BASE/home/admin"
mkdir -p "$BASE/home/meduser"

cat > "$BASE/etc/hostname" << 'EOF'
MedDevice-IoT-001
EOF

cat > "$BASE/etc/passwd" << 'EOF'
root:x:0:0:root:/root:/bin/bash
admin:x:1000:1000:Device Admin:/home/admin:/bin/sh
meduser:x:1001:1001:Medical User:/home/meduser:/bin/sh
EOF

cat > "$BASE/etc/os-release" << 'EOF'
NAME="MedOS"
VERSION="2.4.1"
ID=medos
VERSION_ID="2.4.1"
PRETTY_NAME="MedOS 2.4.1 (IoT Edition)"
HOME_URL="http://meddevice.local"
EOF

cat > "$BASE/etc/issue" << 'EOF'
MedOS 2.4.1 - Authorized Access Only
Patient Vitals Monitor PVM-2000X
EOF

cat > "$BASE/opt/meddevice/device_info.txt" << 'EOF'
Device: Patient Vitals Monitor
Model: PVM-2000X
Firmware: v2.4.1-stable
Serial: MED-IOT-881234
Network: DHCP
Status: OPERATIONAL
EOF

cat > "$BASE/opt/meddevice/network.cfg" << 'EOF'
ip=192.168.1.101
gateway=192.168.1.1
dns=8.8.8.8
mode=dhcp
EOF

cat > "$BASE/var/log/syslog" << 'EOF'
Jan 15 08:00:01 MedDevice-IoT-001 systemd[1]: Started Medical Device Monitoring Service.
Jan 15 08:00:05 MedDevice-IoT-001 medmond[312]: Vitals monitor initialized.
Jan 15 08:01:00 MedDevice-IoT-001 medmond[312]: Patient data collection active.
Jan 15 08:05:00 MedDevice-IoT-001 medmond[312]: Heartbeat signal OK.
EOF

echo "[done] Fake medical IoT filesystem created at $BASE"
