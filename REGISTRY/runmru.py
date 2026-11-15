"""Registry assignment, task 4: the Run window history (RunMRU).

1. Print all the history   (OpenKey, QueryInfoKey, EnumValue)
2. Delete a value from the history
3. Plant (add) a value in the history

Windows only. Run on a virtual machine.
"""
import winreg

KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def read_values(key):
    """Return {name: value} for every value under the key."""
    values = {}
    num_values = winreg.QueryInfoKey(key)[1]
    for i in range(num_values):
        name, value, _ = winreg.EnumValue(key, i)
        values[name] = value
    return values


def print_history():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH) as key:
        for name, value in read_values(key).items():
            print(f"{name} = {value}")


def delete_value(name):
    if len(name) != 1 or name not in LETTERS:
        print("Enter a single lowercase letter (a-z). MRUList cannot be deleted.")
        return
    access = winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH, 0, access) as key:
        values = read_values(key)          # read everything first
        if name not in values:
            print(f"No value named '{name}'.")
            return
        if "MRUList" not in values:
            print("MRUList is missing, nothing was changed.")
            return
        new_order = values["MRUList"].replace(name, "")
        winreg.DeleteValue(key, name)
        winreg.SetValueEx(key, "MRUList", 0, winreg.REG_SZ, new_order)
    print(f"Deleted '{name}'.")


def add_value(command):
    if not command:
        print("Empty command.")
        return
    access = winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH, 0, access) as key:
        values = read_values(key)          # read everything first
        if "MRUList" not in values:
            print("MRUList is missing, nothing was changed.")
            return
        order = values["MRUList"]
        # a free letter is not in the real value names and not in MRUList
        free = [c for c in LETTERS if c not in values and c not in order]
        if not free:
            print("The history is full.")
            return
        name = free[0]
        # Run history values end with \1
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command + "\\1")
        # the newest entry goes first in the order string
        winreg.SetValueEx(key, "MRUList", 0, winreg.REG_SZ, name + order)
    print(f"Added '{command}' as '{name}'.")


def main():
    while True:
        print("\n1. Print history\n2. Delete a value\n3. Add a value\n0. Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                print_history()
            elif choice == "2":
                delete_value(input("Value name to delete (for example a): ").strip())
            elif choice == "3":
                add_value(input("Command to add (for example calc): ").strip())
            elif choice == "0":
                break
        except FileNotFoundError:
            print("The RunMRU key does not exist. Run something from Win+R first.")
        except PermissionError:
            print("No permission to access the key.")
        except OSError as e:
            print(f"Registry error: {e}")


if __name__ == "__main__":
    main()
