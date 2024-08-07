import nuke
import json
import hiero.core


def export_shots():
    # Access the current project and timeline
    project = hiero.ui.activeSequence().project()
    timeline = hiero.ui.activeSequence()

    # Iterate through all the shots in the timeline
    for trackItem in timeline.items():
        shot_name = trackItem.name()
        start_frame = trackItem.timelineIn()
        end_frame = trackItem.timelineOut()

        # Open the Nuke comp template and set frame range
        # nuke.scriptOpen('path/to/your/template.nk')
        # nuke.root().knob('first_frame').setValue(start_frame)
        # nuke.root().knob('last_frame').setValue(end_frame)
        # nuke.scriptSave(f'/path/to/exported/comp/{shot_name}.nk')

        # Save the JSON data for Houdini
        shot_data = {
            'shot_name': shot_name,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'resolution': {
                'width': nuke.root().knob('format').width(),
                'height': nuke.root().knob('format').height()
            }
        }

        json_path = f'/path/to/exported/json/{shot_name}.json'
        with open(json_path, 'w') as json_file:
            json.dump(shot_data, json_file, indent=4)

        print(f'Exported shot: {shot_name}, JSON: {json_path}')
