from django.contrib import admin
from django.conf import settings
from .models import Organization
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ManyToManyWidget

class OrganizationResource(ModelResource):
    contributors = Field(widget=ManyToManyWidget(settings.AUTH_USER_MODEL))

    class Meta:
        model = Organization
        import_id_fields = ('id', 'name',)
        fields = ('id', 'name', 'slug', 'created_by',
                  'contributors', 'description',
                  'created_at', 'updated_at',)

class OrganizationAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = OrganizationResource

    list_display = ('id', 'name', 'slug', 'created_by',
                    'get_contributors', 'description',
                    'created_at', 'updated_at',)
    list_display_links = ('id', 'name', 'created_by',)
    search_fields = ('id', 'name', 'slug', 
                    'owner__id', 
                    'owner__name', 
                    'contributors__name', 
                    'description',)
    # autocomplete_fields = ('organization', )

admin.site.register(Organization, OrganizationAdmin)