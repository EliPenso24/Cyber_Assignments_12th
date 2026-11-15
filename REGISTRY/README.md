# REGISTRY

Windows Registry assignment (12th grade cyber).

`runmru.py` manages the Run dialog history (`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`) using Python's `winreg`.

```
python runmru.py list
python runmru.py delete <letter>
python runmru.py add <command>
```

- Windows only. It reads and changes only the history records of the current user's RunMRU key (single-letter string values `a`-`z` and `MRUList`). Other values are left alone.
- Back up the key first (`reg export`, command is in the script's header) and try it on a virtual machine.
- Testing: `test_mock.py` runs the logic against a fake in-memory `winreg` (add, delete, invalid names, non-string values, missing or malformed `MRUList`, full history, missing key). It has not been run against a real Windows registry.
