from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_token import verify_token
from repositories.milkman_repository import milkman_repository
from models.schemas.milkman import MilkmanModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/milkman/login")

async def get_current_milkman(token: str = Depends(oauth2_scheme)) -> MilkmanModel:
    phone_number = verify_token(token)
    if not phone_number:
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, 
             detail="Could not validate credentials",
             headers={"WWW-Authenticate": "Bearer"},
         )
         
    user_data = await milkman_repository.find_by_phone(int(phone_number))
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return MilkmanModel(**user_data)
