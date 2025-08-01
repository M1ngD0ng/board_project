from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ChildItem, ParentItem


class CommonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "board_project.boards.commons"


class SuitConfig(DjangoSuitConfig):
    layout = "vertical"
    menu = (
        ParentItem(
            "사용자 관리",
            children=[
                ChildItem(model="users.user"),
                ChildItem(model="auth.group"),
            ],
            icon="fa fa-users",
        ),
        ParentItem(
            "게시판 관리",
            children=[
                ChildItem(model="boards.board"),
                ChildItem(model="boards.article"),
                ChildItem(model="boards.comment"),
            ],
            icon="fa fa-list",
        ),
    )
