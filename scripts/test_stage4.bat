@echo off
chcp 65001 >nul
set PYTHONUTF8=1
echo === 1. Стартовый скрипт: ls, cd, pwd, head, uniq (в конце намеренная ошибка) ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml --script examples/startup/stage4_all.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Обработка ошибок всех команд (ввод из файла, REPL не останавливается) ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml < examples/input/errors_stage4.txt
echo Код завершения: %ERRORLEVEL%