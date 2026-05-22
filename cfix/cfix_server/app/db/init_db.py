"""数据库初始化模块，负责数据库基础设施与连接管理。"""

from app.core.sec import hash_pwd
from app.db.base import Base
from app.db.sess import SessionLocal, engine
from app import models  # noqa: F401
from app.core.log import get_logger
from app.repo.user_repo import create_user, get_user_by_username

logger = get_logger("init_db")

DEFAULT_USERNAME = "test01"
DEFAULT_PASSWORD = "123456"


def seed_default_user() -> None:
    with SessionLocal() as db:
        if get_user_by_username(db, DEFAULT_USERNAME):
            logger.info(f"默认账号已存在，跳过初始化: {DEFAULT_USERNAME}")
            return
        create_user(db, DEFAULT_USERNAME, hash_pwd(DEFAULT_PASSWORD), role="user")
        logger.info(f"默认账号初始化完成: {DEFAULT_USERNAME}")


def main():
    Base.metadata.create_all(bind=engine)
    seed_default_user()
    logger.info("数据库表初始化完成")


if __name__ == "__main__":
    main()
