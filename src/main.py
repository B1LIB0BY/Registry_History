import click
from registry_operations import get_run_key, get_run_history, find_missing_char

@click.group()
def program():
    pass

@click.command()
def history():
    run_history = get_run_history()
    if run_history:
        print("Run History:")
        for value_name, value_data, value_type in run_history:
            value_data = value_data.split('\\')[0]
            if value_name != 'MRUList' and value_name != '':
                print(value_data)

@click.command()
@click.argument('value_name', type=click.STRING)
def add(value_name: str):
    run_key = get_run_key()
    if run_key is not None:
        try:
            MRUList = ([pair[1] for pair in get_run_history() if pair[0] == 'MRUList'][0])
            value_key = find_missing_char(list(MRUList))

            MRUList = value_key + MRUList
            winreg.SetValueEx(run_key, 'MRUList', RESERVED, winreg.REG_SZ, MRUList)

            winreg.SetValueEx(run_key, value_key, RESERVED, winreg.REG_SZ, value_name + r'\1')
            print(f"Added '{value_name}' to the registry.")
        except Exception as e:
            print(f"Error: {e}")

@click.command()
@click.argument('value_name', type=click.STRING)
def delete(value_name: str):
    run_key = get_run_key()
    if run_key is not None:
        try:
            run_pairs = get_run_history()
            for value_key, value, _ in run_pairs:
                if value.split('\\')[0] == value_name:
                    winreg.DeleteValue(run_key, value_key)
                    print(f"Deleted value '{value_name}' from the registry.")

                    MRUList = list([pair[1] for pair in run_pairs if pair[0] == 'MRUList'][0])
                    MRUList.remove(value_key)
                    MRUList = ''.join(MRUList)
                    winreg.SetValueEx(run_key, 'MRUList', RESERVED, winreg.REG_SZ, MRUList)
                    break
            else:
                print(f"Value '{value_name}' does not exist in the registry.")

if __name__ == '__main__':
    program.add_command(history)
    program.add_command(add)
    program.add_command(delete)

    program()
