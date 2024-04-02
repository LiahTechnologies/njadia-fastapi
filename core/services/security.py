from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY =os.environ['SECRET_KEY']
ALGORITHM =os.environ['ALGORITHM']

bycrypte_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer =OAuth2PasswordBearer(tokenUrl="/auth/token")