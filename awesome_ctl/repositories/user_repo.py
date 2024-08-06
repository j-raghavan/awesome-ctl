from sqlalchemy.orm import Session

from awesome_ctl.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self):
        return self.db.query(User).all()

    def delete_user(self, user: User):
        self.db.delete(user)
        self.db.commit()
        return user

    def update_user(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user
