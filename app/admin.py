from django.contrib import admin
from .models import Document, Author
from django.utils.html import format_html

class DocumentInline(admin.TabularInline):
    model = Document
    fields = ('title', 'document') 
    extra = 0 
    show_change_link = True

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [DocumentInline]

class DocumentAdmin(admin.ModelAdmin): 
    list_display = ('title','author', 'description', 'image_show', 'document_show_name', 'created_at') 
    search_fields = ('title','author__name', 'description', 'document')
    list_filter = ('created_at', 'author') 
    raw_id_fields = ('author',)

    def image_show(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="max-width:100px; max-height:100px;" />')
        return "-"
    image_show.short_description = 'Image'

    def document_show_name(self, obj):
        if(obj.document):
            return format_html(f'<a href="{obj.document.url}" target="_blank">{obj.document.name.split("/")[-1]}</a>')
        return "-"
    document_show_name.short_description = 'Document'

admin.site.register(Document, DocumentAdmin)
admin.site.register(Author, AuthorAdmin)
