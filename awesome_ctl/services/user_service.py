from awesome_ctl.repositories.user_repo import UserRepository
from awesome_ctl.models.user import User
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repo.get_user_by_id(user_id)

    def create_user(self, username: str, email: str, hashed_password: str) -> User:
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        return self.user_repo.create_user(new_user)

    def get_user_by_username(self, username: str) -> User:
        return self.user_repo.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repo.get_user_by_email(email)

    def get_users(self):
        return self.user_repo.get_users()

    def delete_user(self, user: User):
        return self.user_repo.delete_user(user)

    def update_user(self, user: User):
        return self.user_repo.update_user(user)
