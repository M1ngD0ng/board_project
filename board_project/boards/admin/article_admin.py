from datetime import timedelta

from django import forms
from django.contrib import admin
from django.core.paginator import Paginator
from django.db import models
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
    # list_display = ("title", "content", "author", "created_at")
    # fields = ("title", "content", "board", "author")
    readonly_fields = ("created_at", "modified_at")

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


    ordering = ("-created_at",)
    sortable_by = ("title", "created_at")  # 정렬 기준 제어
    # view_on_site = False
    list_display_links = ("title", "content")
    # list_filter = (
    #     "author",
    #     # "author__id",
    #     "created_at",
    # )
    list_filter = (RecentArticlesFilter, "author")
    list_display = ("get_board_name", "title", "content", "author", "created_at")

    @admin.display(description="board", ordering="created_at")
    def get_board_name(self, article):
        return article.board.name

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
    date_hierarchy = "created_at"  # 해당 필드를 기준으로 탐색할 수 있게 만들어줌


    # paginator = NoCountPaginator
    # show_full_result_count = False
    # show_facets = (  # 각 필터 항목 옆에 해당 항목에 몇 개의 결과가 있는지 표시(always는 성능 저하 발생 가능)
    #     admin.ShowFacets.ALWAYS
    # )
    inlines = [CommentInline]
    actions = [make_notice]
    #
    # formfield_overrides = (
    #     {  # 특정 데이터베이스 필드 타입에 대한 기본 폼 필드(위젯)을 한꺼번에 변경
    #         models.TextField: {"widget": forms.Textarea(attrs={"rows": 4, "cols": 80})},
    #         models.CharField: {"widget": forms.TextInput(attrs={"size": 50})},
    #     }
    # )
    #
    # list_per_page = 10
    # list_max_show_all = 500  # 서버 성능을 보호하기 위한 안전장치 역할.500 이하일 떄에만 "모두 보기" 링크가 표시됨
    #
    # save_as = True  # 새 이름으로 저장 기능 활성화
    # save_as_continue = False  # 새 이름으로 저장 후, 사용자를 어디로 보낼지 제어
    # save_on_top = True  # 저장 관련 버튼을 폼 상단에도 추가함

    # preserve_filters = True  # 필터를 적용한 상태로 객체를 생성, 수정, 삭제한 뒤에 기존 필터 상태를 유지할지 여부 결정\
    # actions_on_top = False
    # actions_on_bottom = True
