@echo off
setlocal enableextensions enabledelayedexpansion
REM Windows wrapper to run Qupac CLI without installation, resolving the right Python.

REM Change to this script's directory (repo root)
pushd "%~dp0"

REM Prefer a local virtual environment if present
if exist "%~dp0venv\Scripts\python.exe" (
  "%~dp0venv\Scripts\python.exe" -m qupac.cli %*
  set EXITCODE=%ERRORLEVEL%
  popd
  exit /b !EXITCODE!
)

REM Prefer Windows py launcher if available
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -m qupac.cli %*
  set EXITCODE=%ERRORLEVEL%
  popd
  exit /b !EXITCODE!
)

REM Fallback to python on PATH
python -m qupac.cli %*
set EXITCODE=%ERRORLEVEL%
popd
exit /b !EXITCODE!
