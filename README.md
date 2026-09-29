Эмулятор командной строки. Вариант №23.
Этап 1. Минимальный REPL: разбор ввода на команду и аргументы, раскрытие переменных окружения, команды-заглушки.
Этап 2. Конфигурация через параметры командной строки и XML-файл конфигурации.
Этап 3. Подключение VFS (загрузка из XML, работа только в памяти).
Этап 4. Полноценные `ls`, `cd`, `uniq`, `pwd`, `head`.
Этап 5. Команды изменения VFS: `touch`, `mv`.

Этап 1.
Для проверки:
PS C:\Users\sokol\Desktop\shell-emulator> python -m src.shell_emulator.main
myvfs> ls firienodv
CMD: ls ARGS: ['firienodv']
myvfs> cd orindgkve
CMD: cd ARGS: ['orindgkve']
myvfs> foobar
Ошибка: неизвестная команда: foobar
myvfs> cd $HOME
CMD: cd ARGS: ['$HOME']
myvfs> exit
PS C:\Users\sokol\Desktop\shell-emulator>
