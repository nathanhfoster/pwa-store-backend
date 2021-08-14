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
        fields = ('id', 'name', 'slug', 'owner',
                  'contributors', 'description',
                  'date_created', 'last_modified',)

class OrganizationAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = OrganizationResource

    list_display = ('id', 'name', 'slug', 'owner',
                    'get_contributors', 'description',
                    'date_created', 'last_modified',)
    list_display_links = ('id', 'name', 'owner',)
    search_fields = ('id', 'name', 'slug', 
                    'owner__id', 
                    'owner__name', 
                    'contributors__name', 
                    'description',)
    # autocomplete_fields = ('organization', )

admin.site.register(Organization, OrganizationAdmin)