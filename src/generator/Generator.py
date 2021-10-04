from jinja2 import DictLoader, Environment, FileSystemLoader
import os
import numpy as np
import random as rd
import numpy as np
from random import shuffle

class Generator:
    def __init__(self):
        self.path = './'
        self.template_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(os.path.join(self.path, 'templates-experimentos')),
            trim_blocks=False
        )

    def render_template(self, template_filename, context):
        return self.template_environment.get_template(template_filename).render(context)

    ####################################################
    def generate_macros(self, filename, long_, q_, delta_, k_, qshock_):
        template_macros = 'macros.inc'
        context = {
            'long': long_,
            'q': q_,
            'delta': delta_,
            'k': k_,
            'qshock': qshock_
        }
        with open(filename, 'w') as f:
            macroFile = self.render_template(template_macros, context)
            f.write(macroFile)
        return True

    ####################################################
    def generate_valfile(self, filename, initial_conditions_percentages, cell_devs_width, cell_devs_height):
        template_val = 'template-valfile.val'

        p_extreme_neg = initial_conditions_percentages[0]
        p_neg = initial_conditions_percentages[1]
        p_neutral = initial_conditions_percentages[2]
        p_pos = initial_conditions_percentages[3]
        p_extreme_pos = initial_conditions_percentages[4]

        total_cells = int(cell_devs_width * cell_devs_height)
        
        extreme_neg = int(total_cells * p_extreme_neg)
        neg = int(total_cells * p_neg)
        neutral = int(total_cells * p_neutral)
        pos = int(total_cells * p_pos)
        extreme_pos = total_cells - extreme_neg - neg - neutral - pos

        v_extreme_neg = [np.random.uniform(-3,-2.8) for i in range(extreme_neg)]
        v_neg = [np.random.uniform(-2.8,-1) for i in range(neg)]
        v_neutral = [np.random.uniform(-1,1) for i in range(neutral)]
        v_pos = [np.random.uniform(1,2.8) for i in range(pos)]
        v_extreme_pos = [np.random.uniform(2.8,3) for i in range(extreme_pos)]
        
        v = v_extreme_neg + v_neg + v_neutral + v_pos + v_extreme_pos
        shuffle(v)
        res = []
        for i in range(cell_devs_height):
            for j in range(cell_devs_width):
                res.append('(' + str(i) + ',' + str(j) + ',0)=' + str(v[cell_devs_width*i+j]))
        context = {'values': res}
        
        with open(filename, 'w') as f:
            valFile = self.render_template(template_val, context)
            f.write(valFile)
        return True

    ####################################################
    def generate_opinion_standalone_ma_file(self, filename, cell_devs_height, cell_devs_width):
        template_ma_standalone = 'template-opinion-standalone.ma'

        # OUTPUTS PARA LAS CONEXIONES DE OPINION CON SHOCKER
        outputs_internal = []
        links_internal_output = []
        for i in range(cell_devs_width):
            i_str = str(i)
            if int(i_str) < 10:
                i_str = "0" + i_str
            for j in range(cell_devs_height):
                j_str = str(j)
                if int(j_str) < 10:
                    j_str = "0" + j_str

                in_val = "in" + i_str + j_str
                out_val = "out" + i_str + j_str
                
                outputs_internal.append(out_val)
                links_internal_output.append("link : "+out_val+"@opinion("+str(i)+","+str(j)+",0) "+out_val)

        context = {
            "N": cell_devs_height, 
            "M": cell_devs_width,
            'outputs_internal': outputs_internal,
            'links_internal_output': links_internal_output,
        }
        with open(filename, 'w') as f:
            standaloneFile = self.render_template(template_ma_standalone, context)
            f.write(standaloneFile)
        return True

    ####################################################
    def generate_goodwin_minsky_ma_file(self, filename, shockers, cell_devs_height, cell_devs_width, cell_devs_delay_value, rules):
        template_ma = 'template-opinion-goodwin-minsky-conexion.ma'

        # INPUTS/OUTPUTS PARA LAS CONEXIONES DE OPINION CON SHOCKER
        inputs_internal = []
        outputs_internal = []
        links_internal_input = []
        links_internal_output = []
        for i in range(cell_devs_width):
            i_str = str(i)
            if int(i_str) < 10:
                i_str = "0" + i_str
            for j in range(cell_devs_height):
                j_str = str(j)
                if int(j_str) < 10:
                    j_str = "0" + j_str

                in_val = "in" + i_str + j_str
                out_val = "out" + i_str + j_str
                
                inputs_internal.append(in_val)
                outputs_internal.append(out_val)
                links_internal_input.append("link : "+in_val+" "+in_val+"@opinion("+str(i)+","+str(j)+",0)")
                links_internal_output.append("link : "+out_val+"@opinion("+str(i)+","+str(j)+",0) "+out_val)

        # CONEXIONES SHOCKER => OPINION (TODOS LOS SHOCKERS IMPACTAN EN TODAS LAS CELDAS)
        # + SETEAR PUERTOS DE OPINION QUE REACCIONAN ANTE SHOCK EXTERNO
        links_external = []
        links_external_transition = []
        for shocker in shockers:
            for cell in shocker.cells:
                i_str = str(cell[0])
                if int(i_str) < 10:
                    i_str = "0" + i_str
                j_str = str(cell[1])
                if int(j_str) < 10:
                    j_str = "0" + j_str

                n_cell = i_str + j_str
                links_external.append("link : out" + n_cell + "@" + shocker.name + " in" + n_cell + "@opinion")
                links_external_transition.append("PortInTransition: in" + n_cell + "@opinion(" + str(cell[0]) + "," + str(cell[1]) + ",0) " + shocker.nombre_shock)

        context = {
            'shockers': shockers,
            'cell_devs_height': cell_devs_height,
            'cell_devs_width': cell_devs_width,
            'delay_value': cell_devs_delay_value,
            
            'inputs_internal': inputs_internal,
            'links_internal_input': links_internal_input,

            'outputs_internal': outputs_internal,
            'links_internal_output': links_internal_output,


            'links_external': links_external,
            'links_external_transition': links_external_transition,
            'rules': rules
        }

        with open(filename, 'w') as f:
            ma_file = self.render_template(template_ma, context)
            f.write(ma_file)
        return True


    ####################################################
    def generate_reg_file(self, filename, shockers):
        template_reg = 'template-reg.cpp'
        context = {
            'shockers': shockers
        }
        with open(filename, 'w') as f:
            reg_file = self.render_template(template_reg, context)
            f.write(reg_file)
        return True

    ####################################################
    def generate_ev_file(self, dirname, input_parameters):
        with open(dirname, 'w') as f:
            for k,v in input_parameters.items():
                f.write("00:00:00:00 " + k + " [" + str(v) + "]\n")
            f.write("\n")
        return True