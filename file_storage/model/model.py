from contextlib import contextmanager
from typing import Any, Iterator, Optional

import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import sessionmaker

from file_storage.model.types import File_
from file_storage.model.utils import generate_unique_identifier

from .database import File, SQLBase, User


class Model:
    def __init__(self, database_url: str):
        """Create model

        Args:
            database_url (str): url of database model should connect to
        """
        self._engine = create_engine(database_url, echo=False)
        SQLBase.metadata.create_all(self._engine)
        self._session_maker = sessionmaker(bind=self._engine)

    @contextmanager
    def _create_session(self, **kwargs: Any) -> Iterator[Session]:
        new_session = self._session_maker(**kwargs)
        try:
            yield new_session
            new_session.commit()
        except Exception:
            new_session.rollback()
            raise
        finally:
            new_session.close()

    def create_user(self, login: str, pass_sha256: str) -> Optional[int]:
        """Create new user

        Args:
            login (str): user login
            pass_sha256 (str): user password hash

        Returns:
            Optional[int]: unique user identifier
        """
        try:
            with self._create_session() as session:
                new_user = User(login=login, pass_sha256=pass_sha256)
                session.add(new_user)
                session.commit()
                return new_user.user_id
        except sqlalchemy.exc.IntegrityError:
            return None

    def get_user_id(self, login: str, pass_sha256: str) -> Optional[int]:
        """Get user id by login and hash of password

        Args:
            login (str): user login
            pass_sha256 (str): user password hash

        Returns:
            Optional[int]: unique user identifier
        """
        with self._create_session() as session:
            res = (
                session.query(User.user_id)
                .filter_by(login=login, pass_sha256=pass_sha256)
                .first()
            )
            return res[0] if res is not None else None

    def add_file(
        self,
        file_sha256: str,
        file_path: str,
        file_original_name: str,
        file_media_type: str,
    ) -> str:
        """Add file to the database

        Args:
            file_sha256 (str): hash of the file

        Returns:
            str: unique file identifier
        """
        with self._create_session() as session:
            file_uid = generate_unique_identifier()
            new_file = File(
                file_uid=file_uid,
                file_sha256=file_sha256,
                file_path=file_path,
                file_original_name=file_original_name,
                file_media_type=file_media_type,
            )
            session.add(new_file)
            session.commit()
            return file_uid

    def get_file_by_uid(self, file_uid: str) -> Optional[File_]:
        """Get file info by file uid

        Args:
            file_uid (str): file unique identifier

        Returns:
            Optional[File_]: file info
        """
        with self._create_session() as session:
            res = (
                session.query(
                    File.file_sha256,
                    File.file_path,
                    File.file_original_name,
                    File.file_media_type,
                )
                .filter_by(file_uid=file_uid)
                .first()
            )
            if not res:
                return None
            return File_(
                file_uid=file_uid,
                file_sha256=res[0],
                file_path=res[1],
                file_original_name=res[2],
                file_media_type=res[3],
            )
