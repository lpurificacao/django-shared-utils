import sqlparse
from django.db.models.query import QuerySet


def patch_queryset_pretty_sql():
    '''If you want this available across your Django project without remembering to call it
     in every script, run the patch during app startup, such as in an app’s AppConfig.ready() method.
    Then in INSTALLED_APPS, use that app config so the patch is applied automatically when Django starts.

    # myapp/apps.py
    from django.apps import AppConfig

       class MyAppConfig(AppConfig):
        name = "myapp"

           def ready(self):
            from .queryset_patch import patch_queryset_pretty_sql
            patch_queryset_pretty_sql()
    
    # myproject/settings.py
    INSTALLED_APPS = [
    ...
        # local
    "myapp.apps.BlogConfig",
    '''
    
    original_init = QuerySet.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        def pretty_sql(self):
            return print(
                sqlparse.format(str(self.query), reindent=True, keyword_case="upper")
            )

        self.pretty_sql = pretty_sql.__get__(self, QuerySet)

    QuerySet.__init__ = new_init
