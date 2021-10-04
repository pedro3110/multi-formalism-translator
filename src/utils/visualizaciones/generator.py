import sys
import os
import config

if config.DIR_MODELS not in sys.path:
    sys.path.append(config.DIR_MODELS)
import json
import xml.etree.ElementTree as etree

# XML's a visualizar
name_filename = [
    {'name': 'teacup', 'filename': 'teacup/top.xml'},
    {'name': 'pulse2', 'filename': 'builtin/pulse2/top.xml'},
    {'name': 'pulse3', 'filename': 'builtin/pulse3/top.xml'},
    {'name': 'cell-teacup', 'filename': 'cell/cell-teacup/top.xml'},
    {'name': 'goodwin-minsky', 'filename': 'goodwin-minsky-matlab/top.xml'},
    {'name': 'lotka-volterra-1', 'filename': 'lotka-volterra-nested-1/top.xml'},
    {'name': 'lotka-volterra-2', 'filename': 'lotka-volterra-nested-2/top.xml'}
]

def traverse(root, d):
    coupleds = root.findall('./components/coupledRef')
    atomics = root.findall('./components/atomicRef')
    internal_connections_ = root.findall('./internal_connections/connection')
    external_input_connections_ = root.findall('./external_input_connections/connection')
    external_output_connections_ = root.findall('./external_output_connections/connection')
    # Add to dictionary
    children = [traverse(c,{}) for c in coupleds]
    children = children + [{'name': atomic.get('name'), 'size': 1} for atomic in atomics]
    internal_connections = [{'from': c.get('component_from'), 'to': c.get('component_to')} for c in internal_connections_]
    external_input_connections = [{'from': c.get('port_from'), 'to': c.get('component_to')} for c in external_input_connections_]
    external_output_connections = [{'from': c.get('component_from'), 'to': c.get('port_to')} for c in external_output_connections_]
    return {
        'name': root.get('name'),
        'children': children,
        'internal_connections': internal_connections,
        'external_input_connections': external_input_connections,
        'external_output_connections': external_output_connections
    }

# Run
cwd = os.getcwd()
for n_f in name_filename:
    name = n_f['name']
    filename = config.DIR_MODELS + n_f['filename']
    
    # Output file
    json_out_filename = cwd + '/data/' + name + '.json' 

    with open(filename, 'r') as top:
        parser = etree.XMLParser(encoding="utf-8")
        xml_top = etree.parse(top, parser=parser)
        root = xml_top.getroot()

        result = traverse(root, {})
        with open(json_out_filename, 'w+') as fp:
            json.dump(result, fp)