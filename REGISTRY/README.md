# REGISTRY

Task 4 of the Registry assignment: the Run window history.

The history is stored in `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU`.
`runmru.py` uses Python's `winreg` module (`OpenKey`, `QueryInfoKey`, `EnumValue`) to:

1. print all the history values,
2. delete a value from the history,
3. add (plant) a value in the history.

## Run

Windows only. The assignment recommends doing registry experiments on a virtual machine.

1. Open the Run window (Win+R) and run a few commands, for example `notepad` and `winword`.
2. Run `python runmru.py`.
3. Choose 1 to print the history, 2 to delete a value by its name (`a`, `b`, ...), or 3 to add a command.

The program has not been run on a real Windows machine yet.
