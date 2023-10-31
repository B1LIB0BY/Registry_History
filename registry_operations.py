import winreg

PATH = winreg.HKEY_CURRENT_USER
RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
RESERVED = 0

def find_missing_char(char_list):
    char_set = set(char_list)
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in char_set:
            return char
    return None

def get_run_key():
    try:
        return winreg.OpenKey(PATH, RUN_KEY_PATH, RESERVED, winreg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        print("Error: Registry key not found.")
        return None
    except PermissionError:
        print("Error: Permission denied. Try running the program as an administrator.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_run_history():
    run_key = get_run_key()
    if run_key is not None:
        try:
            run_pairs = []
            number_of_values = winreg.QueryInfoKey(run_key)[1]
            for i in range(number_of_values):
                run_pairs.append(winreg.EnumValue(run_key, i))
            return run_pairs
        except Exception as e:
            print(f"Error: {e}")
            return []
    else:
        return []

