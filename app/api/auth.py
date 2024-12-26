import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from app.core.db import get_db_connection
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token
from fastapi.responses import JSONResponse

auth_router = APIRouter()

@auth_router.get("/auth/me")
async def get_user():
    # Mocked user data
    return {"username": "test_user", "role": "user"}
@auth_router.post("/auth/login/")
def login(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token({"sub": username})
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True, samesite="Strict")
    return response
@auth_router.post("/signup/")
def signup(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()
    return {"message": "User created successfully"}

@auth_router.post("/login/")
def login(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token({"sub": username})
    return {"message": "Login successful", "user_id": user["id"], "role": user["role"],"access_token": token}
# @auth_router.post("/auth/logout/")
# def logout():
#     return {"message": "Logout successful"}

# @auth_router.post("/auth/token-refresh/")
# def token_refresh(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         new_token = create_access_token(data={"sub": username})
#         return {"access_token": new_token}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")

from fastapi import Response

@auth_router.post("/logout/")
def logout(response: Response):
    """
    Clears the token or session for the user.
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}

from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from app.core.security import SECRET_KEY, ALGORITHM, create_access_token

@auth_router.post("/token-refresh/")
def token_refresh(token: str):
    """
    Refreshes an access token if the provided token is valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Create a new token
        new_token = create_access_token(data={"sub": username})
        return {"access_token": new_token}
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
