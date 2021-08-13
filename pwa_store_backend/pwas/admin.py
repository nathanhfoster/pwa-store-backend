from django.contrib import admin
from .models import Pwa, Rating, Tag
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget

class PwaResource(ModelResource):
    tags = Field(widget=ManyToManyWidget(Tag))

    class Meta:
        model = Pwa
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'url', 'slug',
                  'organization', 'tags', 'description',
                  'views', 'launches', 'date_created', 'last_modified',)

class PwaAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = PwaResource

    list_display = ('id', 'name', 'url', 'slug',
                    'organization', 'get_tags', 'description',
                    'views', 'launches', 'date_created', 'last_modified',)
    list_display_links = ('id', 'name', 'organization', )
    search_fields = ('id', 'name', 'url', 'slug',
                    'organization__name', 'tags__name', 'description',
                    'views', 'launches')
    # autocomplete_fields = ('organization', )

class TagResource(ModelResource):
    class Meta:
        model = Tag
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'date_created', 'last_modified',)
        # widgets = {"tags": {"field": "name"}}

class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TagResource

    list_display = ('id', 'name', 'date_created', 'last_modified',)
    list_display_links = ('id', 'name', )
    search_fields = ('id', 'name',)

admin.site.register(Pwa, PwaAdmin)
admin.site.register(Rating)
admin.site.register(Tag, TagAdmin)