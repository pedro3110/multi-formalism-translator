from src.modulosDEVS.DEVSAtomic.CellDevs import Cell

def cell_devs_opinion(dim, dir_varfile=None):
    
    # Setup parameters
    default_delay_time = 5 # (en milisegundos) en modelo de opinion es 100
    str_default_delay_time = str(default_delay_time)

    ####### Generate CellDEVS object ##########
    cell_devs_name = 'cell'
    cell_devs = Cell(cell_devs_name)
    # Generate Cell Devs
    cell_devs.set_dim((dim[0], dim[1], dim[2]))
    cell_devs.set_delay('transport')
    cell_devs.set_default_delay_time(default_delay_time)
    cell_devs.set_border_type('unwrapped')
    cell_devs.set_neighbors([])
    cell_devs.set_initial_value(-70)
    cell_devs.set_local_transition('opinion-rule')
    cell_devs.set_neighbors([
        (-1,0,0),(0,-1,0),(0,0,0),(0,1,0),(1,0,0),(0,0,1)
    ])
    cell_devs.set_zones([
        {'rule': 'pared-rule', 'cells': '(0,0,0)..(2,2,0) (1,1,1)..(2,2,2)'}
    ])
    # Set I/O ports
    cell_devs.set_input_ports([
        'in1', 'in2', 'in3'
    ])
    cell_devs.set_output_ports([
        'out1', 'out2', 'out3'
    ])
    # Set internal I/O connections
    cell_devs.set_internal_input_connections([
        {'port_from': 'in1', 'component_to': (0,0,0), 'port_to': 'in', "component_from": cell_devs_name, "type": 'in'}
    ])
    cell_devs.set_internal_output_connections([
        {'component_from': (0,0,0), 'port_from': 'out', 'port_to': 'out1', "component_to": cell_devs_name, "type": 'out'}
    ])
    # Set transition rules
    cell_devs.set_rules({
        # Reglas para las zonas (paredes)
        'pared-rule': [
            {'action': 100, 'delay': default_delay_time, 'condition': 't'}
        ],
        # Transicion por evento externo
        'shock-rule': [
            {'action': 'portValue(thisPort)', 'delay': str_default_delay_time, 'condition': 't'}
        ],
        # Transicion tipica (un cell-devs vecino cambio de estado)
        # {'action': '', 'delay': '', 'condition': ''}
        'opinion-rule': [
            # Clock del modelo
            {'action': 'randInt(3)+1', 'delay': default_delay_time, 'condition':'(0,0,1)=?'},   

            #Reglas para no pasarme del intervalo [-3;3] por sumar o restar #macro(delta): 
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=1  and (0,0,0) < -1 and (((0,0,0) - #macro(delta))<-3 )and ( (0,1,0) < (0,0,0) or  (0,1,0) > 1)'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=1  and (0,0,0) < -1 and (0,1,0) <= 1 and (((0,0,0) + #macro(delta))>3)'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=1  and (0,0,0) > 1 and (((0,0,0) + #macro(delta))>3) and ((0,1,0) > (0,0,0)  or  (0,1,0) <= -1 )'},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=1  and (0,0,0) > 1 and (((0,0,0) - #macro(delta))<-3) and (0,1,0) < (0,0,0)'},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=3  and (0,0,0) < -1 and (((0,0,0) - #macro(delta))<-3) and ( (0,-1,0) < (0,0,0) or  (0,-1,0) > 1)'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=3  and (0,0,0) < -1 and (((0,0,0) + #macro(delta))>3) and (0,-1,0) <= 1'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=3  and (0,0,0) > 1 and (((0,0,0) + #macro(delta))>3) and ((0,-1,0) > (0,0,0)  or  (0,-1,0) <= -1 )'},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=3  and (0,0,0) > 1 and (((0,0,0) - #macro(delta))<-3) and (0,-1,0) < (0,0,0)'},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=2  and (0,0,0) < -1 and (((0,0,0) - #macro(delta))<-3) and ( (-1,0,0) < (0,0,0) or  (-1,0,0) > 1)'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=2  and (0,0,0) < -1 and (((0,0,0) + #macro(delta))>3) and (-1,0,0) <= 1'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=2  and (0,0,0) > 1 and (((0,0,0) + #macro(delta))>3) and ((-1,0,0) > (0,0,0)  or  (-1,0,0) <= -1 )'},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=2  and (0,0,0) > 1 and (((0,0,0) - #macro(delta))<-3) and (-1,0,0) < (0,0,0) '},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=4  and (0,0,0) < -1 and (((0,0,0) - #macro(delta))<-3) and ( (1,0,0) < (0,0,0) or  (1,0,0) > 1)'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=4  and (0,0,0) < -1 and (((0,0,0) + #macro(delta))>3) and (1,0,0) <= 1'},
            {'action': 3 , 'delay': default_delay_time , 'condition': '(0,0,1)=4  and (0,0,0) > 1 and (((0,0,0) + #macro(delta))>3) and ((1,0,0) > (0,0,0)  or  (1,0,0) <= -1 )'},
            {'action': -3 , 'delay': default_delay_time , 'condition': '(0,0,1)=4  and (0,0,0) > 1 and (((0,0,0) - #macro(delta))<-3) and (1,0,0) < (0,0,0)'},

            # Reglas para ver a la derecha (capa de conectividad = 1)
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': '(0,0,1)=1  and ((0,1,0)=? or (0,1,0)=(0,0,0))'},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)<=-#macro(long) and (0,1,0)>=#macro(long)'},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)>=#macro(long) and (0,1,0)<=-#macro(long)'},
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))>=abs(#macro(long)) and abs((0,1,0))>1'},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)>1 and abs((0,1,0))<=1'},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)<-1 and abs((0,1,0))<=1'},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (0,1,0)<=-#macro(long)'},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)>1 and (0,0,0)<#macro(long) and (0,1,0)>=#macro(long)'},
            {'action': '(0,0,0) + #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (0,1,0)>=#macro(long)'},
            {'action': '(0,0,0) - #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)>1 and (0,0,0)<#macro(long) and (0,1,0)<=-#macro(long)'},
            {'action': '(0,0,0) + #macro(k)*#macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=1 and (0,1,0)>1 and (0,1,0)<#macro(long)'},
            {'action': '(0,0,0) - #macro(k)*#macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=1 and (0,1,0)<-1 and (0,1,0)>-#macro(long)'},
            {'action': '(0,0,0) + #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=1 and (0,1,0)>=#macro(long)'},
            {'action': '(0,0,0) - #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=1 and (0,1,0)<-#macro(long)'},
            {'action': '(0,0,0)*0', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=#macro(delta) and abs((0,1,0))<=1'},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=1 and abs((0,1,0))<=1 and (0,0,0)>0'},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and abs((0,0,0))<=1 and abs((0,1,0))<=1 and (0,0,0)<0'},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)>1 and (0,1,0)>1 and (0,0,0)<(0,1,0)'},
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)>1 and (0,1,0)>1 and (0,0,0)>(0,1,0)'},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)<-1 and (0,1,0)<-1 and (0,0,0)>(0,1,0)'},
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)<-1 and (0,1,0)<-1 and (0,0,0)<(0,1,0)'},
            {'action': 'if( randInt(1) < 1,(0,0,0) + #macro(delta),(0,0,0) - #macro(delta) ) ', 'delay': default_delay_time, 'condition': '(0,0,1)=1 and (0,0,0)*(0,1,0)<=-1  '},

            # Reglas para ver a abajo (capa de conectividad = 2)
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2  and ((1,0,0)=? or (1,0,0)=(0,0,0))'},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)<=-#macro(long) and (1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)>=#macro(long) and (1,0,0)<=-#macro(long) '},
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))>=abs(#macro(long)) and abs((1,0,0))>1 '},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)>1 and abs((1,0,0))<=1 '},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)<-1 and abs((1,0,0))<=1  '},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (1,0,0)<=-#macro(long) '},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)>1 and (0,0,0)<#macro(long) and (1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) + #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) - #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)>1 and (0,0,0)<#macro(long) and (1,0,0)<=-#macro(long) '},
            {'action': '(0,0,0) + #macro(k)*#macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=1 and (1,0,0)>1 and (1,0,0)<#macro(long)'},
            {'action': '(0,0,0) - #macro(k)*#macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=1 and (1,0,0)<-1 and (1,0,0)>-#macro(long)'},
            {'action': '(0,0,0) + #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=1 and (1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) - #macro(q)*#macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=1 and (1,0,0)<-#macro(long) '},
            {'action': '(0,0,0)*0', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=#macro(delta) and abs((1,0,0))<=1 '},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=1 and abs((1,0,0))<=1 and (0,0,0)>0 '},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and abs((0,0,0))<=1 and abs((1,0,0))<=1 and (0,0,0)<0 '},
            {'action': '(0,0,0) + #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)>1 and (1,0,0)>1 and (0,0,0)<(1,0,0) '},
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)>1 and (1,0,0)>1 and (0,0,0)>(1,0,0) '},
            {'action': '(0,0,0) - #macro(delta)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)<-1 and (1,0,0)<-1 and (0,0,0)>(1,0,0) '},
            {'action': '(0,0,0)', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)<-1 and (1,0,0)<-1 and (0,0,0)<(1,0,0) '},
            {'action': 'if( randInt(1) < 1,(0,0,0) + #macro(delta),(0,0,0) - #macro(delta) ) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=2 and (0,0,0)*(1,0,0)<=-1   '},

            # Reglas para ver a la izquierda (capa de conectividad = 3)
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3  and ((0,-1,0)=? or (0,-1,0)=(0,0,0))'},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)<=-#macro(long) and (0,-1,0)>=#macro(long) '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)>=#macro(long) and (0,-1,0)<=-#macro(long) '},
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))>=abs(#macro(long)) and abs((0,-1,0))>1 '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)>1 and abs((0,-1,0))<=1 '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)<-1 and abs((0,-1,0))<=1 '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (0,-1,0)<=-#macro(long) '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)>1 and (0,0,0)<#macro(long) and (0,-1,0)>=#macro(long) '},
            {'action': '(0,0,0) + #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (0,-1,0)>=#macro(long) '},
            {'action': '(0,0,0) - #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)>1 and (0,0,0)<#macro(long) and (0,-1,0)<=-#macro(long) '},
            {'action': '(0,0,0) + #macro(k)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=1 and (0,-1,0)>1 and (0,-1,0)<#macro(long) '},
            {'action': '(0,0,0) - #macro(k)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=1 and (0,-1,0)<-1 and (0,-1,0)>-#macro(long)'},
            {'action': '(0,0,0) + #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=1 and (0,-1,0)>=#macro(long) '},
            {'action': '(0,0,0) - #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=1 and (0,-1,0)<-#macro(long) '},
            {'action': '(0,0,0)*0 ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=#macro(delta) and abs((0,-1,0))<=1 '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=1 and abs((0,-1,0))<=1 and (0,0,0)>0 '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and abs((0,0,0))<=1 and abs((0,-1,0))<=1 and (0,0,0)<0 '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)>1 and (0,-1,0)>1 and (0,0,0)<(0,-1,0) '},
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)>1 and (0,-1,0)>1 and (0,0,0)>(0,-1,0) '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)<-1 and (0,-1,0)<-1 and (0,0,0)>(0,-1,0) '},
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)<-1 and (0,-1,0)<-1 and (0,0,0)<(0,-1,0) '},
            {'action': 'if( randInt(1) < 1,(0,0,0) + #macro(delta),(0,0,0) - #macro(delta) )  ', 'delay': default_delay_time, 'condition': ' (0,0,1)=3 and (0,0,0)*(0,-1,0)<=-1   '},

            # Reglas para ver a arriba (capa de conectividad = 4)
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4  and ((-1,0,0)=? or (-1,0,0)=(0,0,0))'},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)<=-#macro(long) and (-1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)>=#macro(long) and (-1,0,0)<=-#macro(long) '},
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))>=abs(#macro(long)) and abs((-1,0,0))>1 '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)>1 and abs((-1,0,0))<=1 '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)<-1 and abs((-1,0,0))<=1 '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (-1,0,0)<=-#macro(long) '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)>1 and (0,0,0)<#macro(long) and (-1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) + #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)<-1 and (0,0,0)>-#macro(long) and (-1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) - #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)>1 and (0,0,0)<#macro(long) and (-1,0,0)<=-#macro(long) '},
            {'action': '(0,0,0) + #macro(k)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=1 and (-1,0,0)>1 and (-1,0,0)<#macro(long)'},
            {'action': '(0,0,0) - #macro(k)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=1 and (-1,0,0)<-1 and (-1,0,0)>-#macro(long) '},
            {'action': '(0,0,0) + #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=1 and (-1,0,0)>=#macro(long) '},
            {'action': '(0,0,0) - #macro(q)*#macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=1 and (-1,0,0)<-#macro(long) '},
            {'action': '(0,0,0)*0 ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=#macro(delta) and abs((-1,0,0))<=1 '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=1 and abs((-1,0,0))<=1 and (0,0,0)>0 '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and abs((0,0,0))<=1 and abs((-1,0,0))<=1 and (0,0,0)<0 '},
            {'action': '(0,0,0) + #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)>1 and (-1,0,0)>1 and (0,0,0)<(-1,0,0) '},
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)>1 and (-1,0,0)>1 and (0,0,0)>(-1,0,0) '},
            {'action': '(0,0,0) - #macro(delta) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)<-1 and (-1,0,0)<-1 and (0,0,0)>(-1,0,0) '},
            {'action': '(0,0,0) ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)<-1 and (-1,0,0)<-1 and (0,0,0)<(-1,0,0) '},
            {'action': 'if( randInt(1) < 1,(0,0,0) + #macro(delta),(0,0,0) - #macro(delta) )  ', 'delay': default_delay_time, 'condition': ' (0,0,1)=4 and (0,0,0)*(-1,0,0)<=-1   '},

            {'action': '(0,0,0)', 'delay': str_default_delay_time, 'condition': 't'}
        ]
    })
    # Set ports in transition (la rule ya tiene que estar registrada)
    cell_devs.set_ports_in_transition([
        {'input_port': 'in', 'component': (0,0,0), 'rule': 'shock-rule'}
    ])

    return cell_devs