"""Эмулятор языка оболочки ОС (Вариант №9) с графическим интерфейсом.

Окно на Tkinter имитирует командную строку UNIX-подобной ОС.
Виртуальная файловая система (VFS) загружается из CSV-файла,
и все операции с ней выполняются только в памяти.
"""

import base64
import binascii
import csv
import sys
import tkinter as tk
from tkinter import scrolledtext

VFS_NAME = "vfs-9variant"
PROMPT = VFS_NAME + "$ "
EXIT_SIGNAL = "exit"
EXIT_DELAY_MS = 300
ERROR_PREFIX = "Ошибка"

CSV_HEADER = ["type", "path", "encoding", "content"]
CSV_FIELDS = 4
ENTRY_KINDS = ("dir", "file")
BASE64 = "base64"

MAX_PATH_ARGS = 1

vfs_data = {}
output_box = None
input_box = None
root = None


# ---------- Параметры командной строки ----------
def parse_params(params):
    """Разбирает параметры --vfs и --script.

    Возвращает кортеж (путь к VFS, путь к скрипту, список ошибок).
    """
    found = {"--vfs": None, "--script": None}
    problems = []
    i = 0
    while i < len(params):
        name = params[i]
        if name not in found:
            problems.append("Ошибка: неизвестный параметр " + name)
            i += 1
        elif i + 1 < len(params):
            found[name] = params[i + 1]
            i += 2
        else:
            problems.append("Ошибка: после " + name + " не указан путь")
            i += 1
    return found["--vfs"], found["--script"], problems


# ---------- Загрузка и сохранение VFS ----------
def is_base64(text):
    """Проверяет, что строка является корректными данными base64."""
    try:
        base64.b64decode(text, validate=True)
    except (binascii.Error, ValueError):
        return False
    return True


def parse_row(row, number):
    """Разбирает одну строку CSV.

    Возвращает пару (путь, запись) или строку с текстом ошибки.
    """
    where = " в строке " + str(number)
    if len(row) != CSV_FIELDS:
        return "Ошибка: неверный формат VFS" + where
    kind, path, encoding, content = row
    if kind not in ENTRY_KINDS:
        return "Ошибка: неизвестный тип записи" + where
    path = path.strip("/")
    if path == "":
        return "Ошибка: пустой путь" + where
    if encoding == BASE64 and not is_base64(content):
        return "Ошибка: неверные данные base64" + where
    entry = {"kind": kind, "encoding": encoding, "content": content}
    return path, entry


def load_vfs(file_path):
    """Загружает VFS из CSV-файла в словарь. При ошибке возвращает None."""
    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file))
    except OSError:
        show("Ошибка: не удалось открыть VFS: " + file_path)
        return None
    except csv.Error:
        show("Ошибка: файл VFS не является корректным CSV: " + file_path)
        return None

    if not rows or rows[0] != CSV_HEADER:
        show("Ошибка: неверный заголовок VFS в файле " + file_path)
        return None

    data = {}
    for number, row in enumerate(rows[1:], start=2):
        result = parse_row(row, number)
        if isinstance(result, str):
            show(result)
        else:
            data[result[0]] = result[1]
    return data


def save_vfs(file_path):
    """Сохраняет текущее состояние VFS в CSV. Возвращает True при успехе."""
    try:
        with open(file_path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)
            for path, entry in vfs_data.items():
                writer.writerow([entry["kind"], path, entry["encoding"],
                                 entry["content"]])
    except OSError:
        return False
    return True


# ---------- Команды ----------
def cmd_stub(name, args):
    """Заглушка: выводит имя команды и её аргументы."""
    return name + ": вызвана с аргументами: " + str(args)


def cmd_ls(args):
    """Заглушка команды ls (логика появится на Этапе 4)."""
    if len(args) > MAX_PATH_ARGS:
        return "Ошибка: ls: слишком много аргументов"
    return cmd_stub("ls", args)


def cmd_cd(args):
    """Заглушка команды cd (логика появится на Этапе 4)."""
    if len(args) > MAX_PATH_ARGS:
        return "Ошибка: cd: слишком много аргументов"
    return cmd_stub("cd", args)


def cmd_vfs_save(args):
    """Сохраняет VFS на диск в исходном формате CSV."""
    if len(args) != MAX_PATH_ARGS:
        return "Ошибка: vfs-save: укажите один путь"
    if save_vfs(args[0]):
        return "vfs-save: сохранено в " + args[0]
    return "Ошибка: vfs-save: не удалось сохранить VFS в " + args[0]


def cmd_exit(args):
    """Завершает работу эмулятора."""
    if args:
        return "Ошибка: exit: команда не принимает аргументов"
    return EXIT_SIGNAL


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "vfs-save": cmd_vfs_save,
    "exit": cmd_exit,
}


# ---------- Выполнение команд ----------
def run_line(line):
    """Выполняет одну строку ввода. Возвращает "ok", "error" или "exit"."""
    parts = line.split()
    if not parts:
        return "ok"
    name, args = parts[0], parts[1:]
    if name not in COMMANDS:
        show("Ошибка: неизвестная команда " + name)
        return "error"
    result = COMMANDS[name](args)
    if result == EXIT_SIGNAL:
        show("Выход из эмулятора...")
        root.after(EXIT_DELAY_MS, root.destroy)
        return "exit"
    show(result)
    return "error" if result.startswith(ERROR_PREFIX) else "ok"


def run_script(path):
    """Выполняет стартовый скрипт, показывая и ввод, и вывод."""
    try:
        with open(path, "r", encoding="utf-8-sig") as file:
            lines = file.read().splitlines()
    except OSError:
        show("Ошибка: не удалось открыть стартовый скрипт: " + path)
        return
    for number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        show(PROMPT + line)
        status = run_line(line)
        if status == "error":
            show("Ошибка в строке " + str(number) + " стартового скрипта")
        elif status == "exit":
            break


# ---------- Окно ----------
def show(text):
    """Добавляет строку текста в область вывода."""
    output_box.config(state="normal")
    output_box.insert("end", text + "\n")
    output_box.config(state="disabled")
    output_box.see("end")


def on_enter(event):
    """Обрабатывает нажатие Enter в строке ввода."""
    line = input_box.get()
    input_box.delete(0, "end")
    show(PROMPT + line)
    run_line(line)


def build_window():
    """Создаёт главное окно: область вывода и строку ввода."""
    global root, output_box, input_box
    root = tk.Tk()
    root.title("Эмулятор — " + VFS_NAME)
    root.geometry("700x450")
    output_box = scrolledtext.ScrolledText(
        root, state="disabled", wrap="word", bg="black", fg="white")
    output_box.pack(fill="both", expand=True, padx=6, pady=6)
    frame = tk.Frame(root)
    frame.pack(fill="x", padx=6, pady=6)
    tk.Label(frame, text=PROMPT).pack(side="left")
    input_box = tk.Entry(frame)
    input_box.pack(side="left", fill="x", expand=True, padx=6)
    input_box.bind("<Return>", on_enter)
    input_box.focus_set()


def main():
    """Точка входа: читает параметры, загружает VFS, запускает скрипт."""
    global vfs_data
    vfs_path, script_path, problems = parse_params(sys.argv[1:])
    build_window()
    show("Эмулятор запущен. VFS: " + VFS_NAME + ". Введите команду.")
    show("[отладка] --vfs: " + str(vfs_path))
    show("[отладка] --script: " + str(script_path))
    for text in problems:
        show(text)
    if vfs_path is not None:
        loaded = load_vfs(vfs_path)
        if loaded is not None:
            vfs_data = loaded
            show("VFS загружена, записей: " + str(len(vfs_data)))
    if script_path is not None:
        run_script(script_path)
    root.mainloop()


if __name__ == "__main__":
    main()
