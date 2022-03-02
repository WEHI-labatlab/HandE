



import datetime
from typing import Dict


class Options:
    

    def __init__(self) -> None:
        
        self.fov_list_dict = {}
        self.fov_list_dict["exportDateTime"] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.fov_list_dict["fovFormatVersion"] = "1.5"
        self.fov_list_dict["fovs"] = []

    def add_fov(self, scanCount : int, 
                    centerPointMicronX: int, 
                    centerPointMicronY: int, 
                    sectionId : int,
                    slideId : int,
                    name : str,
                    fovSizeMicrons : int = 400,
                    timingChoice : int = 7,
                    frameSizePixelsX : int = 1024, 
                    frameSizePixelsY : int = 1024,
                    preset : str = "Normal", 
                    aperture : str = "2",
                    displayName : str = "Fine",
                    notes : str = None,
                    timingDescription : str = "1 ms"
                    ):
        self.fov_list_dict["fovs"].append(
            {
            "scanCount": scanCount,
            "centerPointMicrons": {
                "x": centerPointMicronX,
                "y": centerPointMicronY
            },
            "fovSizeMicrons": fovSizeMicrons,
            "timingChoice": timingChoice,
            "frameSizePixels": {
                "width": frameSizePixelsX,
                "height": frameSizePixelsY
            },
            "imagingPreset": {
                "preset": preset,
                "aperture": aperture,
                "displayName": displayName,
                "defaults": {
                "timingChoice": timingChoice
                }
            },
            "sectionId": sectionId,
            "slideId": slideId,
            "name": name,
            "notes": notes,
            "timingDescription": timingDescription
            }
        )

    def get_fov_list_dict(self) -> Dict:
        return self.fov_list_dict