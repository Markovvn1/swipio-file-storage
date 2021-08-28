import hashlib
import os
from typing import Optional, Tuple

from loguru import logger

from ..model import Model, ModelFile
from .exceptions import CorruptedFileControllerException, FileControllerException


class Controller:
    _model: Model
    _storage_path: str

    def __init__(self, storage_path: str, database_url: str):
        self._model = Model(database_url)
        self._storage_path = storage_path

    def register_new_user(self, login: str, pass_sha256: str) -> Optional[int]:
        return self._model.create_user(login, pass_sha256)

    def get_user_id(self, login: str, pass_sha256: str) -> Optional[int]:
        return self._model.get_user_id(login, pass_sha256)

    def _file_sha256_to_path(self, file_sha256: str) -> Tuple[str, str]:
        file_path = os.path.join(file_sha256[0:2], file_sha256[2:4])
        return file_path, file_sha256

    def get_file_path_in_storage(self, file_path: str) -> str:
        return os.path.join(self._storage_path, file_path)

    def save_file(
        self, file_content: bytes, file_original_name: str, file_media_type: str
    ) -> str:
        """Save file to storage

        Args:
            file_content (bytes): content of the file

        Returns:
            str: unique file identifier
        """
        file_sha256 = hashlib.sha256(file_content).hexdigest()
        file_path, file_name = self._file_sha256_to_path(file_sha256)
        file_path_in_storage = self.get_file_path_in_storage(file_path)

        try:
            os.makedirs(file_path_in_storage, exist_ok=True)
            with open(os.path.join(file_path_in_storage, file_name), 'wb') as f:
                f.write(file_content)
        except PermissionError as e:
            logger.error(repr(e))
            raise FileControllerException() from e
        except FileNotFoundError as e:
            logger.error(repr(e))
            raise FileControllerException() from e

        return self._model.add_file(
            file_sha256,
            os.path.join(file_path, file_name),
            file_original_name,
            file_media_type,
        )

    def get_file_by_uid(self, file_uid: str) -> Optional[ModelFile]:
        file = self._model.get_file_by_uid(file_uid)
        if file is None:
            return None

        try:
            with open(self.get_file_path_in_storage(file.file_path), 'rb') as f:
                file_content = f.read()
        except PermissionError as e:
            logger.error(repr(e))
            raise FileControllerException() from e
        except FileNotFoundError as e:
            logger.error(repr(e))
            raise FileControllerException() from e

        file_sha256 = hashlib.sha256(file_content).hexdigest()
        if file_sha256 != file.file_sha256:
            logger.error(
                'File {} corrupted. Target sha256sum is {}, but file has {}',
                file.file_path,
                file.file_sha256,
                file_sha256,
            )
            raise CorruptedFileControllerException('Hash sum is incorrect')

        return file
