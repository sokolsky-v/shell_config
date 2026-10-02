Эмулятор командной строки. Вариант №23.
Этап 1. Минимальный REPL: разбор ввода на команду и аргументы, раскрытие переменных окружения, команды-заглушки.
Этап 2. Конфигурация через параметры командной строки и XML-файл конфигурации.
Этап 3. Подключение VFS (загрузка из XML, работа только в памяти).
Этап 4. Полноценные `ls`, `cd`, `uniq`, `pwd`, `head`.
Этап 5. Команды изменения VFS: `touch`, `mv`.

Этап 1.

- Приглашение к вводу вида `<vfs_name>> ` (имя VFS пока задано константой `DEFAULT_VFS_NAME` в `main.py`).
- `ls [args...]`, `cd [args...]` — заглушки, печатают своё имя и переданные аргументы.
- `exit` — завершает работу.
- Парсер раскрывает переменные окружения реальной ОС (`$VAR`, на Windows также работает `%VAR%`).
- Ошибки обрабатываются без падения программы: неизвестная команда и некорректный ввод (например, незакрытая кавычка) выводят сообщение об ошибке, после чего диалог продолжается.

Для проверки:
PS C:\Users\sokol\Desktop\shell-emulator> python -m src.shell_emulator.main
myvfs> ls firienodv
CMD: ls ARGS: ['firienodv']
myvfs> cd orindgkve
CMD: cd ARGS: ['orindgkve']
myvfs> foobar
Ошибка: неизвестная команда: foobar
myvfs> cd $USERPROFILE
CMD: cd ARGS: ['C:\\Users\\sokol']
myvfs> exit
PS C:\Users\sokol\Desktop\shell-emulator>

Сборка и запуск
Требуется Python 3.10+.

```bash
pip install -r requirements-dev.txt
python -m src.shell_emulator.main
python -m pytest tests
```
