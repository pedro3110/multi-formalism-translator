import shutil
import src.traductor.config as config
import json
from src.modulosDEVS.DEVSGenerator import *
from src.modulosDEVS.CellDEVSGenerator import CellDEVSGenerator
from src.modulosCDPP.cdpp_model import CdppModel
from src.modulosCDPP.cdpp_model_to_ma_file import CdppModelToMaConverter
from src.modulosCDPP.preprocessing import preprocessing_devsml_for_ma
from src.modulosAuxiliares.valfile_generator import valfile_generator

from src.modulosAuxiliares.cell_devs_atomic.cell_devs_atomic_generator import cell_devs_atomic_generator


class Traductor:

    def __init__(self, archivo_modelos_base, root_templates, log='logs/traductor.log'):
        self.DEVSML_TEMPLATE_FILENAME = config.DEVSML_TEMPLATE_FILENAME
        self.CPP_H_TEMPLATES_FILENAMES = config.CPP_H_TEMPLATES_FILENAMES
        self.ROOT_TEMPLATES = root_templates
        self.params_traducciones = {}
        with open(archivo_modelos_base, 'r') as f:
            self.params_traducciones = json.load(f)

    ###################
    # DEVS
    ##################
    def run_devs(self, devs_generator, hcpp_generator):

        self.devs_generator = devs_generator
        self.hcpp_generator = hcpp_generator

        for model, params in self.params_traducciones.items():
            DIR_XMILE = params['DIR_XMILE']
            DEVSML_CPP_H_DIRECTORY = params['DEVSML_CPP_H_DIRECTORY']
            DEVSML_TOP_FILENAME = params['DEVSML_TOP_FILENAME']
            DEVSML_EVENTS_FILENAME = params['DEVSML_EVENTS_FILENAME']
            DEVSML_MA_FILENAME = params['DEVSML_MA_FILENAME']
            DEVSML_SH_FILENAME = params['DEVSML_SH_FILENAME']

            try:
                shutil.rmtree(DEVSML_CPP_H_DIRECTORY)
                os.makedirs(DEVSML_CPP_H_DIRECTORY)
            except Exception:
                os.makedirs(DEVSML_CPP_H_DIRECTORY)
            # Initialize directory
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'Makefile'), DEVSML_CPP_H_DIRECTORY + '/Makefile')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'macros.inc'), DEVSML_CPP_H_DIRECTORY + '/macros.inc')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'tuple_to_real.h'), DEVSML_CPP_H_DIRECTORY + '/tuple_to_real.h')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'tuple_to_real.cpp'), DEVSML_CPP_H_DIRECTORY + '/tuple_to_real.cpp')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'equation_calculator.h'), DEVSML_CPP_H_DIRECTORY + '/equation_calculator.h')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'equation_calculator.cpp'), DEVSML_CPP_H_DIRECTORY + '/equation_calculator.cpp')

            # Generate .devsml file
            self.devs_generator.generateDEVSML(DIR_XMILE, self.DEVSML_TEMPLATE_FILENAME, DEVSML_TOP_FILENAME)

            # Generate .ma, .ev, .cpp, .h, reg.cpp
            self.hcpp_generator.generateHCPP(DEVSML_TOP_FILENAME,
                                             DEVSML_CPP_H_DIRECTORY,
                                             # self.ROOT_TEMPLATES,
                                             self.CPP_H_TEMPLATES_FILENAMES,
                                             DEVSML_EVENTS_FILENAME,
                                             DEVSML_MA_FILENAME)

            # TODO: Generate run.sh

    ###################
    # CELL-DEVS
    ##################
    def run_cell_devs(self, devs_generator, hcpp_generator):

        self.devs_generator = devs_generator
        self.hcpp_generator = hcpp_generator
        self.cell_devs_generator = CellDEVSGenerator()

        for model, params in self.params_traducciones.items():
            DIR = params['DIR']
            DIR_XMILE = params['DIR_XMILE']
            DEVSML_CPP_H_DIRECTORY = params['DEVSML_CPP_H_DIRECTORY']
            DEVSML_TOP_FILENAME = params['DEVSML_TOP_FILENAME']
            DEVSML_EVENTS_FILENAME = params['DEVSML_EVENTS_FILENAME']
            DEVSML_MA_FILENAME = params['DEVSML_MA_FILENAME']
            DIR_MA_CELL_DEVS = params['DIR_MA_CELL_DEVS']
            DIR_CELL_DEVS = params['DIR_CELL_DEVS']
            DIR_VALFILE = params['DIR_VALFILE']

            size_cell_devs = (params['VALFILE_GENERATOR']['size_x'],
                              params['VALFILE_GENERATOR']['size_y'],
                              params['VALFILE_GENERATOR']['size_z'])
            VALFILE_GENERATOR = valfile_generator(params['VALFILE_GENERATOR']["name"], size_cell_devs)

            generator = cell_devs_atomic_generator()
            CELL_DEVS_ATOMIC = generator.generate_cell_devs_atomic(params['CELL_DEVS_ATOMIC'])

            try:
                shutil.rmtree(DEVSML_CPP_H_DIRECTORY)
                os.makedirs(DEVSML_CPP_H_DIRECTORY)
            except Exception:
                os.makedirs(DEVSML_CPP_H_DIRECTORY)
            # Initialize directory
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES, 'macros.inc'), DIR + '/macros.inc')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES,'Makefile'), DEVSML_CPP_H_DIRECTORY + '/Makefile')

            # Nota: este componente es necesario porque el cell-devs no puede recibir tuple<Real>. Debe recibir Real's
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES,'tuple_to_real.h'), DEVSML_CPP_H_DIRECTORY + '/tuple_to_real.h')
            shutil.copyfile(os.path.join(self.ROOT_TEMPLATES,'tuple_to_real.cpp'), DEVSML_CPP_H_DIRECTORY + '/tuple_to_real.cpp')

            # Generate .devsml file
            self.devs_generator.generateDEVSML(DIR_XMILE, self.DEVSML_TEMPLATE_FILENAME, DEVSML_TOP_FILENAME)

            # Generate Cell-Devs xml
            self.cell_devs_generator.generateCellDEVSML(CELL_DEVS_ATOMIC, DIR_CELL_DEVS, VALFILE_GENERATOR, DIR_VALFILE)

            # Generation of .ma file corresponding to only the cell-devs
            devs_ml_model = preprocessing_devsml_for_ma(etree.parse(DIR_CELL_DEVS))
            cdpp_model = CdppModel.from_devsml_xml(devs_ml_model)
            mafile = CdppModelToMaConverter.parse_model(cdpp_model)
            with open(DIR_MA_CELL_DEVS, 'w') as f:
                f.write(str(mafile))

            # Combinar top.xml con cell_devs.xml
            with open(DEVSML_TOP_FILENAME, 'r') as top:
                parser1 = etree.XMLParser(encoding="utf-8")
                xml_top = etree.parse(top, parser=parser1)
                root_xml_top = xml_top.getroot()
                with open(DIR_CELL_DEVS, 'r') as cell_devs:
                    parser2 = etree.XMLParser(encoding="utf-8")
                    xml_cell_devs = etree.parse(cell_devs, parser=parser2)
                    root_xml_cell_devs = xml_cell_devs.getroot()

                    # Combine
                    root_xml_top.find('./components').append(root_xml_cell_devs)

                    # TODO : agregar conexiones de CoupledModel => CellDevs
                    #

                    # Save top-modified
                    x = etree.tostring(root_xml_top)
                    os.remove(DEVSML_TOP_FILENAME)
                    vkb.xml(x, DEVSML_TOP_FILENAME)

            # Generate .ma, .ev, .cpp, .h, reg.cpp
            self.hcpp_generator.generateHCPP(DEVSML_TOP_FILENAME, DEVSML_CPP_H_DIRECTORY,
                                             self.CPP_H_TEMPLATES_FILENAMES, DEVSML_EVENTS_FILENAME,
                                             DEVSML_MA_FILENAME)