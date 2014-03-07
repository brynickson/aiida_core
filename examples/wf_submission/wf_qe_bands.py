#!/usr/bin/env python

def launch_ws():

    """
    To control the wf_stauts use the procedure 
    
    wf.list_workflows() 
    
    and to force the retrival of some calculation you can use the function
    
    wf.retrieve_by_uuid(uuid_wf).kill_step_calculations(methohd_wf)
    
    """
        
    from aiida.workflows.quantumespresso.bands import WorkflowQEBands
    from aiida.orm import DataFactory
    StructureData = DataFactory('structure')
    ParameterData = DataFactory('parameter')
    
    alat = 4. # angstrom
    cell = [[alat, 0., 0.,],
        [0., alat, 0.,],
        [0., 0., alat,],
       ]
    s = StructureData(cell=cell)
    s.append_atom(position=(0.,0.,0.),symbols='Ba')
    s.append_atom(position=(alat/2.,alat/2.,alat/2.),symbols='Ti')
    s.append_atom(position=(alat/2.,alat/2.,0.),symbols='O')
    s.append_atom(position=(alat/2.,0.,alat/2.),symbols='O')
    s.append_atom(position=(0.,alat/2.,alat/2.),symbols='O')
    s.store()

    params = {}
    params['computername'] = "rosa"
    params['resources'] = {
        'num_machines': 1,
        'num_cpus_per_machine': 16
        }
    params['pseudo_family'] = "pslib030-pbesol-rrkjus"
    params['structure_uuid'] = s.uuid
    
    kpoints = ParameterData({
                'type': 'automatic',
                'points': [4, 4, 4, 0, 0, 0],
                }).store()
    params['kpoints_uuid'] = kpoints.uuid


    w = WorkflowQEBands()
    w.set_params(params)
    w.start()
    
    print "Launched workflow", w.uuid

if __name__ == '__main__':
    from aiida.common.utils import load_django
    load_django()
    launch_ws()