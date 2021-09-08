import os
import pathlib

def _make_sure_directory(path):
    directory = os.path.dirname(path)  

    if not os.path.exists(directory): 
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def _read_container_name(path):
    if not os.path.exists(path):
        raise Exception('Ancypwn is not running yet')

    container_name = None
    with open(path, 'r') as f:
        container_name = f.read()
    if not container_name:
        os.remove(path)
        raise Exception('incorrect status')
    return container_name
