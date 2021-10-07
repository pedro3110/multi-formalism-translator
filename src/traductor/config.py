import os

PROJECT_DIRECTORY = os.getenv('MULTI_FORMALISM_TRANSLATOR_DIRECTORY')
ROOT_TEMPLATES = os.path.join(PROJECT_DIRECTORY, 'templates/templates-devs')

DEVSML_TEMPLATE_FILENAME = 'template-devsml.xml'
CPP_H_TEMPLATES_FILENAMES = {
    'sh': 'template-sh.sh',
    'reg': 'template-reg.cpp',
    'DEVSFtot': 'template-Ftot',
    'DEVSFplus': 'template-Aux-Fpm',
    'DEVSFminus': 'template-Aux-Fpm',
    'DEVSAux': 'template-Aux-Fpm',
    'DEVSConstant': 'template-Cte',
    'events': 'template-ev.ev',
    'DEVSPulse': 'template-Pulse',
    'DEVSStep': 'template-Step',
    'DEVSUniform': 'template-Uniform',
    'DEVSDelay': 'template-Delay',
    'DEVSIntegrator': 'qss1',
    'DEVSGraphical': 'template-graphical',
    'DEVSArrayCollector': 'template-array-collector',
    'DEVSArrayAgregator': 'template-array-agregator'
}