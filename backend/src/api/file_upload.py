from src.core.database import DB
from src.utils.get_current_user_util import GetCurrentUser
from fastapi import APIRouter, HTTPException, status, UploadFile
from datetime import date
from sqlalchemy import select, update, delete
from src.models.file_upload import File
import os
import time


router = APIRouter(prefix='/file', tags=['File-Upload'])

UPLOAD_DIR = 'uploads/receipts'


@router.post('/uploads')
async def file_uploads(file: UploadFile, db: DB, user: GetCurrentUser) -> dict:

    # make folder if not exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_content = await file.read()
    
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    allowed_types = ['image/jpeg', 'image/png']

    # convert to mb
    file_size = len(file_content) / (1024 * 1024)   # MB
    if file_size > 5:
        print('File too large')

    # check if file is valid or not
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions or file.content_type not in allowed_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file type')

    # generate unique filename
    unique_filename = f'{user.id}_{int(time.time())}_{file.filename}'

    # combine path with file_name
    filepath = os.path.join(UPLOAD_DIR, unique_filename)

    # save in file
    with open(filepath, 'wb') as file:
        file.write(file_content)

    # save in database
    file_save = File(
        filepath=filepath
    )

    db.add(file_save)
    db.commit()
    db.refresh(file_save)

    return {
        'id': file_save.id
    }
