# Windows API MessageBox

`WIN_API.py` holds ten numbered exercises on showing Windows message boxes from Python:

- `MessageBox` from `win32gui`, `win32api` and `win32ui`, and the argument differences between them.
- Combining button constants with `|` (for example `MB_YESNO | MB_HELP`).
- Reading the return value (6 for Yes, 7 for No).
- Calling `MessageBoxW` in `user32.dll` directly with `ctypes`.

Imports `ctypes`, `win32api`, `win32con`, `win32gui` and `win32ui` (the `win32` modules come from the pywin32 package).
