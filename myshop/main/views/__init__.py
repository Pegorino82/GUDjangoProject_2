from .authors import (
    create_author_model_form,
    update_author_model_form,
    detail_author,
    delete_author,
    list_author,

    # generic views:
    CreateAuthorView,
    ListAuthorView,
    DetailAuthorView,
    UpdateAuthorView,
    DeleteAuthorView,
)

from .articles import (
    list_article,
    create_article,
    update_article,
    detail_article,
    delete_article,

    # generic views:
    ArticleView,
)
