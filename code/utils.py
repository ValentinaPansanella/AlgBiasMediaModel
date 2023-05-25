import json

def read_dicts(path, name):
    try:
        with open(f'{path}/final_opinions_{name}.json', 'rt') as file:
            final_opinions = json.load(file)
    except:
        final_opinions = {}
    try:
        with open(f'{path}/final_iterations_{name}.json', 'rt') as file:
            final_iterations = json.load(file)
    except:
        final_iterations = {}
    
    return final_opinions, final_iterations

def write_dicts(path, name, final_opinions, final_iterations):
    with open(f'{path}/final_opinions_{name}.json', 'wt') as file:
        print(final_opinions)
        json.dump(final_opinions, file)
    with open(f'{path}/final_iterations_{name}.json', 'wt') as file:
        print(final_iterations)
        json.dump(final_iterations, file)