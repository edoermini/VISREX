import importlib

def get_tool(toolname):
    try:
        module = importlib.import_module(f'masup.tools.{toolname}')
    except ModuleNotFoundError:
        return None
    
    return module.Tool