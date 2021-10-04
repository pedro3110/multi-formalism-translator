from src.modulosAuxiliares.cell_devs_atomic.cell_devs_opinion import cell_devs_opinion
from src.modulosAuxiliares.cell_devs_atomic.cell_devs_trafico import cell_devs_trafico


class cell_devs_atomic_generator:

    def generate_cell_devs_atomic(self, CELL_DEVS_ATOMIC):

        t = (CELL_DEVS_ATOMIC['size_x'],
             CELL_DEVS_ATOMIC['size_y'],
             CELL_DEVS_ATOMIC['size_z'])

        if CELL_DEVS_ATOMIC['name'] == "cell_devs_opinion":
            return cell_devs_opinion(t, CELL_DEVS_ATOMIC['valfile_dir'])
        elif CELL_DEVS_ATOMIC['name'] == "cell_devs_trafico":
            return cell_devs_trafico(t, CELL_DEVS_ATOMIC['valfile_dir'])
        else:
            raise Exception("ERROR: CELL_DEVS_ATOMIC no se puede generar")