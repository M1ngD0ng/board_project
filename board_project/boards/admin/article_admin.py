from datetime import timedelta

from django.contrib import admin
from django.core.paginator import Paginator
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.utils.functional import cached_property

from ..commons.admin import SiteBaseModelAdmin
from ..models import Article, Comment


@admin.action(description="선택한 게시글 제목에 [공지] 붙이기")
def make_notice(modeladmin, request, queryset):
    queryset.update(title=Concat(Value("[공지] "), F("title")))


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0  # 기본으로 보여줄 빈 추가 폼의 개수


class NoCountPaginator(
    Paginator
):  # 대용량 테이블에서, count 쿼리는 성능 저하를 유발함->개선
    # 전체 개수를 count 하는 대신,매우 큰 수를 반환하여 성능 저하 방지
    @cached_property
    def count(self):
        return 999999


class RecentArticlesFilter(admin.SimpleListFilter):  # 커스텀 필터
    title = "최근 게시물"
    parameter_name = "recent articles"  # url에 사용되는 파라미터 이름

    def lookups(
        self, request, model_admin
    ):  # 필터 옵션 목록 (url값, 사용자에게 보이는 이름)
        return (
            ("1d", "최근 1일"),
            ("7d", "최근 7일"),
            ("30d", "최근 30일"),
        )

    def queryset(self, request, queryset):
        if self.value() == "1d":
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=1))
        if self.value() == "7d":
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=7))
        if self.value() == "30d":
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=30))

        return queryset


@admin.register(Article)
class ArticleAdmin(SiteBaseModelAdmin):
    date_hierarchy = "created_at"  # 해당 필드를 기준으로 탐색할 수 있게 만들어줌
    ordering = ("-created_at",)
    list_display_links = ("title", "content")
    list_filter = (RecentArticlesFilter, "author")
    list_display = ("get_board_name", "title", "content", "author", "created_at")
    list_select_related = (
        "board",
    )  # get_board_name 할때 성능 문제 발생 방지 -> 미리 관련 객체 정보까지가져와서 성능 향상시킴
    list_editable = (
        "author",
    )  # list_display에 표시된 필드들을 상세 페이지에 들어가지 않고도 수정하고 저장할 수 있게 함
    search_fields = ("^title", "content")
    search_help_text = (
        "제목, 내용으로 검색할 수 있습니다."  # 검색창 아래에 표시될 안내 문구
    )
    # paginator = NoCountPaginator
    # show_full_result_count = False

    fieldsets = [  # 수정 가능한 필드와 readonly 필드 분리해서 표시
        (
            None,
            {
                "fields": ["title", "content", "board", "author"],
            },
        ),
        (
            "Timestamped",
            {
                "fields": ["created_at", "modified_at"],
            },
        ),
    ]
    inlines = [CommentInline]
    readonly_fields = ("created_at", "modified_at")

    actions = [make_notice]

    @admin.display(description="board", ordering="created_at")
    def get_board_name(self, article):
        return article.board.name
