import sqlparse
from django.db.models.query import QuerySet


def patch_queryset_pretty_sql():
    original_init = QuerySet.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        def pretty_sql(self):
            return print(
                sqlparse.format(str(self.query), reindent=True, keyword_case="upper")
            )

        self.pretty_sql = pretty_sql.__get__(self, QuerySet)

    QuerySet.__init__ = new_init
