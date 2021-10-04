
def preprocessing_devsml_for_ma(root):

    # TODO : no anda
    def traverse(r, level):
        atomics = r.findall('./components/atomicRef')
        atomics_names = [a.get('name') for a in atomics]
        coupleds = r.findall('./components/coupledRef')

        internal_connections = r.find('./internal_connections')
        ext_input_conn = r.find('./external_input_connections')
        ext_output_conn = r.find('./external_output_connections')

        for ic in internal_connections:
            if ic.get('component_from') in atomics_names:
                ic.set('component_from', ic.get('component_from') + str(level))
            if ic.get('component_to') in atomics_names:
                ic.set('component_to', ic.get('component_to') + str(level))

        for eic in ext_input_conn:
            if eic.get('component_to') in atomics_names:
                eic.set('component_to', eic.get('component_to') + str(level))

        for eoc in ext_output_conn:
            if eoc.get('component_from') in atomics_names:
                eoc.set('component_from', eoc.get('component_from') + str(level))

        # TODO : insertar name_level en lugar de re-setearselo (y, sacarle el name_level al top.xml)
        for a in atomics:
            a.set('name_level', a.get('name') + str(level))
        # print a.get('name_level')

        for c in coupleds:
            traverse(c, level + 1)

    # Run
    traverse(root, 0)

    return root
