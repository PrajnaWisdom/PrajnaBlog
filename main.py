import argparse

from app.app import create_app
from app.models.admin_user import AdminUser
from app.config import ADMIN_ACCOUNT, ADMIN_PASSWORD


app = create_app()


def create_default_admin_user():
    AdminUser.create(
        account=ADMIN_ACCOUNT,
        password=ADMIN_PASSWORD
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='init system')
    parser.add_argument('--create_default_admin_user', action='store_true')
    args = parser.parse_args()
    if args.create_default_admin_user:
        create_default_admin_user()

