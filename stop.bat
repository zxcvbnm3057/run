@echo off
@taskkill /F /IM run.exe >nul 2>nul
set /a result=%ERRORLEVEL%
if %result% == 0 (echo 成功)
if %result% == 128 (echo 程序未运行)
pause