from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import json

def align_audio_with_text(audio_path, transcript):
    config_string = "task_language=eng|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audio_path
    task.text_file_path_absolute = None
    task.text_file_contents = transcript
    task.sync_map_file_path_absolute = "syncmap.json"

    ExecuteTask(task).execute()
    task.output_sync_map_file()

    with open("syncmap.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = [
        {
            "start": float(fragment["begin"]),
            "end": float(fragment["end"]),
            "text": fragment["lines"][0]
        }
        for fragment in data["fragments"] if fragment["lines"]
    ]

    return segments
