@echo off
chcp 65001 >nul
set PYTHONUTF8=1
echo === 1. Стартовый скрипт: touch и mv (в конце намеренная ошибка) ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml --script examples/startup/stage5_all.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Обработка ошибок touch и mv (ввод из файла, REPL не останавливается) ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml < examples/input/errors_stage5.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 3. XML-файл VFS остался неизменным (изменения только в памяти) ===
findstr /c:"new.txt" /c:"renamed.txt" examples\vfs\deep.xml
if errorlevel 1 (echo OK: в deep.xml нет созданных файлов) else (echo ОШИБКА: файл изменён)