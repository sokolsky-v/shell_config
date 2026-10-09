@echo off
chcp 65001 >nul
echo === 1. Только параметры командной строки ===
python -m src.shell_emulator.main --vfs examples/vfs/cli.xml --script examples/startup/ok.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Без параметров, пустой ввод завершает REPL ===
python -m src.shell_emulator.main < NUL
echo Код завершения: %ERRORLEVEL%