@echo off
chcp 65001 >nul
set PYTHONUTF8=1
echo === 1. Стартовый скрипт: все команды этапов 1-3 (в конце намеренная ошибка) ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml --script examples/startup/stage3_all.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Раскрытие переменной окружения DEMO_DIR (ввод из файла) ===
set DEMO_DIR=projects
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml < examples/input/env_stage3.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 3. Обработка ошибок в интерактивном режиме (ввод из файла) ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml < examples/input/errors_stage3.txt
echo Код завершения: %ERRORLEVEL%