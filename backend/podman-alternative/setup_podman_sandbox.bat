@echo off
echo ===============================
echo  Starting OptimizeHub Sandbox
echo ===============================

podman machine start
cd %~dp0
podman-compose down
podman-compose build
podman-compose up
