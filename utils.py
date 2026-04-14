import sqlparse
from django.db.models.query import QuerySet


def patch_queryset_pretty_sql():
    """
    Monkey patches Django QuerySet.__init__ to add a pretty_sql() method.

    After calling this, any QuerySet created will have a .pretty_sql() method
    that formats and syntax-highlights the SQL query using sqlparse and Rich.

    Usage:
        patch_queryset_pretty_sql()
        qs = Book.objects.filter(title__startswith='A')
        qs.pretty_sql()  # Prints formatted, colored SQL

    To use project-wide, add to AppConfig.ready():
        from django.apps import AppConfig

        class MyAppConfig(AppConfig):
            name = "myapp"

            def ready(self):
                from shared_utils.utils import patch_queryset_pretty_sql
                patch_queryset_pretty_sql()
    """
    
    original_init = QuerySet.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        def pretty_sql(self):
            return print(
                sqlparse.format(str(self.query), reindent=True, keyword_case="upper")
            )

        self.pretty_sql = pretty_sql.__get__(self, QuerySet)

    QuerySet.__init__ = new_init
