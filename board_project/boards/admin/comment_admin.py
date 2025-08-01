from django.contrib import admin

from ..models import Comment


@admin.action(description="선택한 댓글을 숨김 처리")
def make_hidden(modeladmin, request, queryset):
    queryset.update(is_visible=False)


@admin.action(description="선택한 댓글을 공개 처리")
def make_visible(modeladmin, request, queryset):
    queryset.update(is_visible=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("get_board_name", "article", "content", "author", "created_at")
    list_display_links = ("article", "content")
    list_select_related = ("article",)
    list_editable = ("author",)
    ordering = ("-created_at",)
    search_fields = ("content",)
    search_help_text = ("댓글 내용으로 검색할 수 있습니다.",)

    readonly_fields = ("created_at", "modified_at")

    actions = [make_hidden, make_visible]

    @admin.display(description="board", ordering="created_at")
    def get_board_name(self, comment: Comment):
        return comment.article.board.name
