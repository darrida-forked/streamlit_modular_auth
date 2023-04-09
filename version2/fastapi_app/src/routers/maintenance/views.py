from typing import List

from fastapi import APIRouter, HTTPException

from src.routers.maintenance.models import (
    APIGroup,
    APIUpdateAccount,
    APIUserAccount,
    APIUserDelete,
    APIUserReturn,
    DBAccess,
    DBUser,
)

# INITALIZE THE ROUTER FASTAPI MAIN
router = APIRouter()


@router.get(
    "/user",
    response_model=APIUserAccount,
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def get_user(username: str):
    """## Queries User Account Information

    - Serves as an endpoint for service admins to query user accounts

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** List of objects containing user information.
    """
    user = DBUser.get(username, api_return=True)
    print(user)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Existing user not found.")


# ##############################################################
# # ENDPOINT: CREATE USER
# ##############################################################
@router.post(
    "/user",
    response_model=APIUserReturn,
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def create_user(user_model: APIUserAccount):
    """## Creates User Account

    - Serves as an endpoint for service admins to create user accounts
    - The following information can be sent:
        - Username (also serves as account name) => REQUIRED
        - Password (plain password is stored as a one-way hashed string) => REQUIRED
        - Full name
        - Email
        - Disabled status => REQUIRED
    - NOTE: Take note that the "disabled" value in the "Try it out" section defaults to true (disabled)

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** Returns user account information
    """
    user_info = DBUser.create(user_model)
    if not user_info:
        raise HTTPException(status_code=422, detail="Email or username already exists.")
    return user_info


##############################################################
# ENDPOINT: UPDATE USER
##############################################################
@router.put(
    "/user",
    response_model=APIUpdateAccount,
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def update_user(user_model: APIUpdateAccount):
    """## Updates User Account

    - Serves as an endpoint for service admins to update user accounts
    - The following information can be sent:
        - Username (also serves as account name) => REQUIRED
        - Password (plain password is stored as a one-way hashed string)
        - Full name
        - EMAIL (**not updateable** -- will be ignored if change attempt is made)
        - Disabled status
    - ONLY send information that you want to update (other than username, which is required).
      - If include a key name in the json, but leave it blank, it will change that entry to an empty string.
      - An example would be changing a password: Only username and password values are required.

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** Returns user account information
    """
    if user_info := DBUser.update(user_model):
        return user_info
    else:
        raise HTTPException(status_code=404, detail="Existing user not found.")


##############################################################
# ENDPOINT: GET USERS
##############################################################
@router.get(
    "/users",
    response_model=List[APIUserAccount],
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def get_users(include_disabled: bool = False):
    """## Queries User Account Information

    - Serves as an endpoint for service admins to query user accounts

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** List of objects containing user information.
    """
    user_l = DBUser.get_all(include_disabled)
    if user_l:
        return user_l
    else:
        raise HTTPException(status_code=404, detail="Existing user not found.")


@router.delete(
    "/user/scope",
    # response_model=List[APIUserAccount],
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def take_away_scope(username: str, scope: str):
    """## Removes authentication scope from user

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** List of objects containing user information.
    """
    DBUser.remove_scope(username, scope)


@router.post(
    "/user/scope",
    # response_model=List[APIUserAccount],
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def give_scope(username: str, scope: str):
    """## Removes authentication scope from user

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** List of objects containing user information.
    """
    DBUser.add_scope(username, scope)


##############################################################
# ENDPOINT: DELETE USERS
##############################################################
@router.delete(
    "/user",
    response_model=APIUserDelete,
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users"},
        404: {"detail": "Existing user not found"},
    },
)
async def delete_user(user_model: APIUserAccount):
    """## Deletes User Account

    - Serves as an endpoint for service admins to delete user accounts
    - While the following information can be sent, ONLY **username** is required:
        - Username => REQUIRED
        - Password
        - Full name
        - Email
        - Disabled status

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** Simple response message.
    """
    out_come = DBUser.delete(user_model)
    if out_come is True:
        return APIUserDelete(result=f"User {user_model.username} deleted successfully")
    elif out_come is False:
        raise HTTPException(status_code=500, detail=f"User {user_model.username} not deleted. Error encountered")
    else:
        return APIUserDelete(result=f"User {user_model.username} not found.")


@router.post(
    "/scope",
    response_model=APIGroup,
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users."},
        404: {"detail": "Existing user not found"},
    },
)
async def create_group(group_model: APIGroup):
    """## Creates User Account

    - Serves as an endpoint for service admins to create user accounts
    - The following information can be sent:
        - Username (also serves as account name) => REQUIRED
        - Password (plain password is stored as a one-way hashed string) => REQUIRED
        - Full name
        - Email
        - Disabled status => REQUIRED
    - NOTE: Take note that the "disabled" value in the "Try it out" section defaults to true (disabled)

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** Returns user account information
    """
    user_info = DBAccess.create(group_model)
    if not user_info:
        raise HTTPException(status_code=422, detail="Scope already exists.")
    return user_info


@router.delete(
    "/scope",
    # response_model=APIUserDelete,
    tags=["Maintenance"],
    responses={
        401: {"description": "Incorrect username or password"},
        403: {"description": "Authenticated user does not have permission to manager users"},
        404: {"detail": "Existing user not found"},
    },
)
async def delete_scope(scope: str):
    """## Deletes User Account

    - Serves as an endpoint for service admins to delete user accounts
    - While the following information can be sent, ONLY **username** is required:
        - Username => REQUIRED
        - Password
        - Full name
        - Email
        - Disabled status

    ### Permissions:
    - Requires admin permissions to use

    ### Headers:
    - **Authorization:** Bearer [token_string]
    - **accept:** application/json

    ### Returns:
    - **JSON:** Simple response message.
    """
    out_come = DBAccess.delete(scope)
    if out_come is True:
        return APIUserDelete(result=f"Scope {scope} deleted successfully")
    elif out_come is False:
        raise HTTPException(status_code=500, detail=f"Scope {scope} not deleted. Error encountered")
    else:
        return APIUserDelete(result=f"Scope {scope} not found.")
