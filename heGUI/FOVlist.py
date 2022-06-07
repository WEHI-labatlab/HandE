



import datetime
from typing import Dict


class Options:


    def __init__(self) -> None:

        self.fov_list_dict = {}
        self.export_date_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.fov_format_version = "1.5"
        self.fovs = []

    def add_fov(self, scanCount : int,
                    centerPointMicronX: int,
                    centerPointMicronY: int,
                    sectionId : int,
                    slideId : int,
                    name : str,
                    fovSizeMicrons : int = 400,
                    timingChoice : int = 7,
                    preset : str = "Normal",
                    aperture : str = "2",
                    displayName : str = "Fine",
                    notes : str = None,
                    timingDescription : str = "1 ms"
                    ):

        if fovSizeMicrons == 400:
            frameSizePixelsX = 1024
            frameSizePixelsY = 1024
        elif fovSizeMicrons == 800:
            frameSizePixelsX = 2048
            frameSizePixelsY = 2048
        else:
            fovSizeMicrons = 400
            frameSizePixelsX = 1024
            frameSizePixelsY = 1024

        self.fovs.append(
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
        return {"exportDateTime" : self.export_date_time, "fovFormatVersion" : self.fov_format_version, "fovs" : self.fovs}
