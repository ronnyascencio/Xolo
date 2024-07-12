import os


def commercialstructure(base_path):
    subdirectories = ['_Assets', '_Editorial', '_References', '_Shots', '_Renders', '_Renders/Review',
                      '_Renders/Client', '_Renders/Delivery', '_inCome', '_outGoing']
    for subdir in subdirectories:
        commercial_path = os.path.join(base_path, '_Production', subdir)
        os.makedirs(commercial_path, exist_ok=True)
        print(f'directory created: {commercial_path}')


def animationstructure(base_path):
    subdirectories = ['_Assets', '_Editorial', '_References', '_Shots', '_Renders', '_Renders/Review',
                      '_Renders/Client', '_Renders/Delivery']
    for subdir in subdirectories:
        animation_path = os.path.join(base_path, '_Production', subdir)
        os.makedirs(animation_path, exist_ok=True)
        print(f'directory created: {animation_path}')


def vfxstructure(base_path):
    subdirectories = ['_Assets', '_Editorial', '_References', '_Shots', '_Renders', '_Resources', '_Renders/Review',
                      '_Renders/Client', '_Renders/Delivery', '_Plates', '_Plates/_Shots']
    for subdir in subdirectories:
        vfx_path = os.path.join(base_path, '_Production', subdir)
        os.makedirs(vfx_path, exist_ok=True)
        print(f'directory created: {vfx_path}')


def shotstructure(base_path):
    subdirectories = ['_Assets', '_References', '_Shots', '_Renders', '_Renders/Final', '_Renders/Wip']
    for subdir in subdirectories:
        shot_path = os.path.join(base_path, '_Production', subdir)
        os.makedirs(shot_path, exist_ok=True)
        print(f'directory created: {shot_path}')
