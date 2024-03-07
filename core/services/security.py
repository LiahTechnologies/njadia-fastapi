from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext


SECRET_KEY ="A122KJKJ445J5BJ66KLGU657J 5J213KJ4K5JGH34JJ453J6J4.32HJKCHJLJO56.2LJ2GK!H2G@JKKJ43J5J43LJ>CWJ8U0-85CJKL/JAJSD"
ALGORITHM ="HS256"

bycrypte_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer =OAuth2PasswordBearer(tokenUrl="/auth/token")