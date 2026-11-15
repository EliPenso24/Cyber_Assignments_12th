"""Manage the Run dialog history (RunMRU) with winreg - Windows only.

Only touches the current user's RunMRU key, and only its history records:
single lowercase-letter REG_SZ values (a-z) plus the MRUList string.
Any other value in the key is left alone. Try it on a virtual machine first
and export the key before changing it:
  reg export "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU" backup.reg

Usage:
  python runmru.py list
  python runmru.py delete <letter>      e.g. delete b
  python runmru.py add <command>        e.g. add calc
"""
import re
import sys
import winreg

KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
SUFFIX = "\\1"  # records are stored as command + backslash + 1
LETTER = re.compile(r"^[a-z]$")


def open_key(access):
    return winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH, 0, access)


def read_all():
    """Return (entries, order, order_ok).

    entries: {letter: text} for valid history records only.
    order:   MRUList letters that point to a valid record, without repeats.
    order_ok: False if MRUList is missing, not a string, or had bad letters.
    """
    entries, raw_order = {}, None
    with open_key(winreg.KEY_READ) as key:
        _, count, _ = winreg.QueryInfoKey(key)
        for i in range(count):
            name, value, kind = winreg.EnumValue(key, i)
            if name == "MRUList":
                if kind == winreg.REG_SZ and isinstance(value, str):
                    raw_order = value
            elif LETTER.match(name) and kind == winreg.REG_SZ and isinstance(value, str):
                entries[name] = value
    order = []
    for ch in raw_order or "":
        if ch in entries and ch not in order:
            order.append(ch)
    order_ok = raw_order is not None and "".join(order) == raw_order
    return entries, "".join(order), order_ok


def strip_suffix(text):
    return text[:-len(SUFFIX)] if text.endswith(SUFFIX) else text


def full_order(entries, order):
    """MRUList order first, then any remaining records alphabetically."""
    rest = sorted(c for c in entries if c not in order)
    return order + "".join(rest)


def show():
    entries, order, order_ok = read_all()
    if not entries:
        print("(history is empty)")
        return
    for pos, letter in enumerate(full_order(entries, order), 1):
        print(f"{pos}. [{letter}] {strip_suffix(entries[letter])}")
    if not order_ok:
        print("Note: MRUList is missing or inconsistent, so the order above may not match Windows.")


def write_order(key, order):
    winreg.SetValueEx(key, "MRUList", 0, winreg.REG_SZ, order)


def delete(letter):
    if not LETTER.match(letter):
        sys.exit("Entry name must be a single lowercase letter a-z.")
    entries, order, _ = read_all()
    if letter not in entries:
        sys.exit(f"No history entry named '{letter}'.")
    new_order = full_order(entries, order).replace(letter, "")
    with open_key(winreg.KEY_SET_VALUE) as key:
        winreg.DeleteValue(key, letter)
        write_order(key, new_order)
    print(f"Deleted entry '{letter}'.")


def add(command):
    if not command.strip() or any(ord(c) < 32 for c in command):
        sys.exit("Command must be non-empty text without control characters.")
    entries, order, _ = read_all()
    free = [c for c in "abcdefghijklmnopqrstuvwxyz" if c not in entries]
    if not free:
        sys.exit("History is full (26 entries). Delete one first.")
    letter = free[0]
    new_order = letter + full_order(entries, order)
    with open_key(winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, letter, 0, winreg.REG_SZ, command + SUFFIX)
        write_order(key, new_order)
    print(f"Added '{command}' as entry '{letter}'.")


def main(args):
    try:
        if args[:1] == ["list"] and len(args) == 1:
            show()
        elif len(args) == 2 and args[0] == "delete":
            delete(args[1])
        elif len(args) >= 2 and args[0] == "add":
            add(" ".join(args[1:]))
        else:
            print(__doc__)
    except FileNotFoundError:
        sys.exit("RunMRU key not found. Open the Run window (Win+R) and run something first.")
    except PermissionError:
        sys.exit("No permission to change the RunMRU key.")


if __name__ == "__main__":
    main(sys.argv[1:])
