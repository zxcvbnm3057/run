@echo off
@taskkill /F /IM run.exe >nul 2>nul
set /a result=%ERRORLEVEL%
if %result% == 0 (echo �ɹ�)
if %result% == 128 (echo ����δ����)
pause