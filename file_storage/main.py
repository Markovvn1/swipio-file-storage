import hashlib
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .controller import Controller, ControllerException

MAX_UPLOAD_SIZE = 1024 * 1024

app = FastAPI()
controller = Controller('storage', 'sqlite:///file_storage.db')
security = HTTPBasic()


def get_current_user_id(credentials: HTTPBasicCredentials = Depends(security)) -> int:
    pass_sha256 = hashlib.sha256(credentials.password.encode()).hexdigest()
    user_id = controller.get_user_id(credentials.username, pass_sha256)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Basic'},
        )
    return user_id


@app.post('/upload')
def upload_file(
    _user_id: int = Depends(get_current_user_id), file: UploadFile = File(...)
) -> Dict[str, Any]:
    file_chunks = []  # type: List[bytes]

    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f'Too large file. Maximum allowed file: {MAX_UPLOAD_SIZE} bytes',
            )
        file_chunks.append(chunk)

    try:
        file_uid = controller.save_file(
            b''.join(file_chunks), file.filename, file.content_type
        )
    except ControllerException:
        return {'status': 'error', 'reason': 'problems with server'}

    return {'status': 'ok', 'file_uid': file_uid}


@app.get('/download/{file_uid}')
def download_file(file_uid: str) -> FileResponse:
    try:
        file = controller.get_file_by_uid(file_uid)
    except ControllerException:
        file = None

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='you are not allowed to get this file',
        )

    return FileResponse(
        path=controller.get_file_path_in_storage(file.file_path),
        filename=file.file_original_name,
        media_type=file.file_media_type,
    )
