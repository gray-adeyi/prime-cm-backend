from fastapi import APIRouter

router = APIRouter()


@router.post()
async def login():
    """
    Note: Only `AdminUser` can
    login. to get the Auth Token
    for subsequent API calls.
    """
    pass


@router.post()
async def create_user():
    """
    Only `AdminUser` is authoried
    to create `User` regardless of
    level.
    Only `AdminUser` with `Level.ZERO`
    can create another `AdminUser`
    """
    pass


@router.put()
async def update_user():
    """
    Endpoint allows modification of
    `User` information.
    """
    pass


@router.get()
async def search_user():
    """
    Returns a list of matching `User` instance based
    on the provided query.
    """


@router.get()
async def list_customers():
    """
    Returns a list of
    `User`
    """
    pass


@router.get()
async def list_admins():
    """
    Returns a list of `AdminUser`
    Only authorized users can hit
    this endpoint.
    """
    pass
