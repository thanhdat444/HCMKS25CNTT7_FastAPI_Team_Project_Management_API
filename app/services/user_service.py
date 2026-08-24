from sqlalchemy.orm import Session
from app.models.user import UserModel 

def get_users_service(
    db: Session,
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None
):
    query = db.query(UserModel)

    if name:
        query = query.filter(UserModel.fullname.like(f"%{name}%"))

    if email:
        query = query.filter(UserModel.email.like(f"%{email}%"))

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    return query.all()