@echo off
cd /d C:\Windows\Microsoft.NET\Framework\v4.0.30319

set csprojPath=%~dp0make.csproj

MSBuild.exe %csprojPath%

echo %ERRORLEVEL%

if %ERRORLEVEL% == 0 (
  goto SUCCESS
)

pause

:SUCCESS