from django.contrib import admin
from .models import Pwa, Rating, Tag, PwaScreenshot, PwaAnalytics
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget
from .admin_forms import PwaAdminForm

class PwaResource(ModelResource):
    tags = Field(widget=ManyToManyWidget(Tag))

    class Meta:
        model = Pwa
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'url', 'slug',
                  'organization', 'tags', 'image_url', 'description',
                  'views', 'launches', 'created_at', 'updated_at',)
        widgets = {'organization': {'field': 'pk'}, 'tags': {'field': 'name'}, }


class PwaAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = PwaResource
    form = PwaAdminForm
    list_display = ('id', 'name', 'slug', 'url', 'get_tags', 'published',
                    'created_at', 'updated_at',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name', 'url', 'slug',
                     'organization__name', 'tags__name', 'description',)
    

class TagResource(ModelResource):
    class Meta:
        model = Tag
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'created_at', 'updated_at',)
        # widgets = {'tags': {'field': 'name'}}


class TagAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = TagResource

    list_display = ('id', 'name', 'created_at', 'updated_at',)
    list_display_links = ('id', 'name', )
    search_fields = ('id', 'name',)


class PwaScreenShotsResource(ModelResource):
    class Meta:
        model = PwaScreenshot
        fields = '__all__'


class PwaScreenShotsAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    model = PwaScreenShotsResource
    list_display_links = ('pwa', 'id')
    list_display = ('id', 'pwa', 'image_url',  'caption', )


class PwaAnalyticsResource(ModelResource):
    class Meta:
        model = PwaAnalytics
        fields = '__all__'


class PwaAnalyticsAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    model = PwaAnalyticsResource
    list_display_links = ('pwa', 'id')
    list_display = ('id', 'pwa', 'view_count', 'launch_count', 'rating_avg', 'rating_count')


admin.site.register(Pwa, PwaAdmin)
admin.site.register(Rating)
admin.site.register(Tag, TagAdmin)
admin.site.register(PwaScreenshot, PwaScreenShotsAdmin)
admin.site.register(PwaAnalytics, PwaAnalyticsAdmin)
