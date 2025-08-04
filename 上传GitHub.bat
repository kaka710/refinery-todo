@echo off
chcp 65001 >nul
title 海南炼化Todo系统 - GitHub上传工具

echo.
echo ========================================
echo   海南炼化Todo系统 - GitHub上传工具
echo ========================================
echo.

cd /d "%~dp0"

echo 正在启动上传工具...
python "上传到GitHub.py"

if errorlevel 1 (
    echo.
    echo 上传工具执行失败，请检查Python环境
    pause
    exit /b 1
)

echo.
echo 上传工具执行完成
pause
