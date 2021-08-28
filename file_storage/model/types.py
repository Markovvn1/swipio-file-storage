from dataclasses import dataclass


@dataclass(frozen=True)
class File_:
    file_uid: str
    file_sha256: str
    file_path: str
    file_original_name: str
    file_media_type: str
