import os


def commercialstructure(base_path):
    subdirectories = ['Assets', 'Editorial', 'References', 'Shots', 'Renders', 'Renders/Review',
                      'Renders/Client', 'Renders/Delivery', 'inCome', 'outGoing']
    for subdir in subdirectories:
        commercial_path = os.path.join(base_path, 'Production', subdir)
        resources_path = os.path.join(base_path, 'Resources')
        os.makedirs(commercial_path, exist_ok=True)
        os.makedirs(resources_path, exist_ok=True)
        print(f'directory created: {commercial_path}')


def animationstructure(base_path):
    subdirectories = ['Assets', 'Editorial', 'References', 'Shots', 'Renders', 'Renders/Review',
                      'Renders/Client', 'Renders/Delivery']
    for subdir in subdirectories:
        animation_path = os.path.join(base_path, 'Production', subdir)
        resources_path = os.path.join(base_path, 'Resources')
        os.makedirs(animation_path, exist_ok=True)
        os.makedirs(resources_path, exist_ok=True)
        print(f'directory created: {animation_path}')


def vfxstructure(base_path):
    subdirectories = ['Assets', 'Editorial', 'References', 'Shots', 'Renders', 'Resources', 'Renders/Review',
                      'Renders/Client', 'Renders/Delivery', 'Plates', 'Plates/_Shots']
    for subdir in subdirectories:
        vfx_path = os.path.join(base_path, 'Production', subdir)
        resources_path = os.path.join(base_path, 'Resources')
        os.makedirs(vfx_path, exist_ok=True)
        os.makedirs(resources_path, exist_ok=True)
        print(f'directory created: {vfx_path}')


def shotstructure(base_path):
    subdirectories = ['Assets', 'References', 'Shots', 'Renders', 'Renders/Final', 'Renders/Wip']
    for subdir in subdirectories:
        shot_path = os.path.join(base_path, 'Production', subdir)
        resources_path = os.path.join(base_path, 'Resources')
        os.makedirs(shot_path, exist_ok=True)
        os.makedirs(resources_path, exist_ok=True)
        print(f'directory created: {shot_path}')
