#!/bin/bash

echo "🔍 네트워크 정보 확인 중..."
echo ""

# WSL IP
WSL_IP=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
echo "📌 WSL IP: $WSL_IP"

# Windows IP (추정)
WIN_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
echo "📌 Windows IP (추정): $WIN_IP"

echo ""
echo "🌐 모바일에서 접속 시도할 주소:"
echo "   1. http://$WSL_IP:3000"
echo "   2. http://$WIN_IP:3000"
echo ""
echo "💡 위 주소가 안 되면 Windows에서 'ipconfig' 실행 후"
echo "   무선 LAN 어댑터의 IPv4 주소를 확인하세요!"
