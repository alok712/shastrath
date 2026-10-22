@echo off
REM Signs the SHASTRATH release APK with your own keystore.
REM Usage:  sign-apk.bat  path\to\key.jks  alias  storepass  keypass
setlocal
set KEY=%~1
set ALIAS=%~2
set STORE=%~3
set KEYPASS=%~4

if "%KEY%"=="" (
  echo.
  echo   Usage:  sign-apk.bat  path\to\key.jks  alias  storePassword  keyPassword
  echo.
  echo   Example:
  echo     sign-apk.bat  C:\keys\my-release.jks  myalias  secret  secret
  echo.
  pause
  exit /b 1
)

REM --- locate apksigner from the Android SDK -------------------------------
set SDK=%ANDROID_HOME%
if "%SDK%"=="" set SDK=%ANDROID_SDK_ROOT%
if "%SDK%"=="" set SDK=C:\projects
set BT=
for /f "delims=" %%d in ('dir /b /ad /o-n "%SDK%\build-tools" 2^>nul') do (
  if not defined BT set BT=%SDK%\build-tools\%%d
)
if not exist "%BT%\apksigner.bat" (
  echo ERROR: apksigner.bat not found under %SDK%\build-tools
  pause
  exit /b 1
)

set IN=app\build\outputs\apk\release\app-release-unsigned.apk
set OUT=%USERPROFILE%\Downloads\SHASTRATH-release.apk

echo Signing %IN%
"%BT%\apksigner.bat" sign --ks "%KEY%" --ks-key-alias "%ALIAS%" --ks-pass pass:"%STORE%" --key-pass pass:"%KEYPASS%" --out "%OUT%" "%IN%"
if errorlevel 1 (
  echo Signing FAILED
  pause
  exit /b 1
)
echo.
echo DONE -> %OUT%
"%BT%\apksigner.bat" verify --print-certs "%OUT%"
pause
