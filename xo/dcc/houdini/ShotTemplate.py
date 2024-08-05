import hou
import os


def shotTemplate():
    # paths creation
    hip_name = '.'.join(hou.hipFile.name().split('.')[:-1])
    shot_name = hip_name.split('/')[-1]
    shot_version = shot_name.split('_')[-1]
    root_name = shot_name.split('_')[0]
    stage_name = '/' + root_name.split('-')[-1]
    department_name = hip_name.split('/')[8]
    task_name = hip_name.split('/')[9]
    shot_path = '/'.join(hip_name.split('/')[0:7])
    render_path = os.path.join(shot_path, 'Renders', '3dRender', task_name, shot_version).replace('\\', '/')
    # layer_path =

    # print(layer_path)

    # Create custom variables
    # job_root = 'D:/jobs'

    # hou.hscript(f'setenv JOB = {job_root}')

    # hou.hscript(f'setenv ASSET = {hip_path}/my_custom_path')
    hou.hscript(f'setenv XOLO_DEPARTMENT = {department_name}')
    hou.hscript(f'setenv XOLO_TASK = {task_name}')

    # node creation

    stage = hou.node('/stage')
    prim_root = stage.createNode('primitive', 'SHOT_CONTEXT')
    prim_root.parm('primpath').set(stage_name)
    department_layer = stage.createNode('reference', 'DEPARTMENT_LAYER')
    department_layer.parm('primpath1').set(stage_name + '/assets')

    # Create two null nodes
    null1 = stage.createNode('null', 'DEPARTMENT_IN')
    null2 = stage.createNode('null', 'WORK_OUT')

    # nodes connection
    department_layer.setInput(0, prim_root)
    null1.setInput(0, department_layer)
    null2.setInput(0, null1)

    # nodes re position

    prim_root.moveToGoodPosition()
    department_layer.setPosition([prim_root.position().x(), prim_root.position().y() - 5])
    null1.setPosition([department_layer.position().x(), department_layer.position().y() - 5])
    null2.setPosition([null1.position().x(), null1.position().y() - 10])

    # rop creation if model to lay out
    department = hou.getenv('DEPARTMENT')
    if not 'lgt ' in department:
        layer_rop = stage.createNode('usd_rop', 'department')

        # Connect layer_rop to prim_root
        layer_rop.setInput(0, null2)
        layer_rop.setPosition([null2.position().x(), null2.position().y() - 10])

        # Layout the nodes for better visibility
        # stage.layoutChildren(items=(prim_root, null1, null2, layer_rop), vertical_spicing=-3)
    else:
        print('department is lighting')
        hou.hscript(f'setenv RENDER = {render_path}')

        stage.layoutChildren(items=(prim_root, null1, null2), vertical_spicing=-3)

    # Set a valid menu item for the 'outputprocessors' parameter
    # layer_rop.parm('outputprocessors').set('savepathsrelativetooutput')
    # Uncomment the following line if you want to disable network safe save
    # layer_rop.parm('usenetworksafesave').set(False)


