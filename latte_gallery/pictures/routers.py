from fastapi import APIRouter, status
from fastapi.params import Depends

from latte_gallery.core.dependencies import PictureServiceDep, SessionDep
from latte_gallery.pictures.schemas import PictureCreateSchema, PictureSchema
from latte_gallery.security.dependencies import AuthenticatedAccount, AuthorizedAccount
from latte_gallery.security.permissions import Authenticated

pictures_router = APIRouter(tags=["Картинки"])


@pictures_router.post(
    "/pictures",
    summary="Создать новую картинку",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AuthorizedAccount(Authenticated()))],
)
async def create_picture(
    body: PictureCreateSchema,
    current_user: AuthenticatedAccount,
    picture_service: PictureServiceDep,
    session: SessionDep,
):
    assert current_user is not None

    picture = await picture_service.create(current_user.id, body, session)
    return PictureSchema.model_validate(picture)
