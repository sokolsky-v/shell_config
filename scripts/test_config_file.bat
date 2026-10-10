@echo off
chcp 65001 >nul
echo === 1. Параметры из XML-конфига ===
python -m src.shell_emulator.main --config examples/configs/config_ok.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. CLI имеет приоритет над конфигом ===
python -m src.shell_emulator.main --config examples/configs/config_ok.xml --vfs examples/vfs/minimal.xml --script examples/startup/ok.txt
echo Код завершения: %ERRORLEVEL%