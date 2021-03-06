from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, ArticleImage
from imagekit.admin import AdminThumbnail
# Register your models here.




class ArticleImageInline(admin.StackedInline):
    fields = ('image', 'image_tag')
    readonly_fields = ('image_tag',)
    model = ArticleImage
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('MƏQALƏNİN ADI ( MAKSIMUM 100 SIMVOL! )', {
            "fields": (
                ('title', 'title_english'),
            ),
        }),

        ('AZƏRBAYCANCA KONTENT *', {
            "fields": (
                'content',
            ),
            'classes':(
                'collapse',
            )
        }),

        ('İNGİLİSCƏ KONTENT', {
            "fields": (
                'content_english',
            ),
            'classes':(
                'collapse',
            )
        }),

        ('ŞƏKİL ( MAKSIMUM 2 MEGABYTE! )', {
            "fields": (
                'main_image_tag', 'main_image', 'cover_image_tag', 'cover_image', 
            ),
        }),

        (None, {
            "fields": (
                'slug_link', 'category'
            ),
        }),

    )

    admin_thumbnail = AdminThumbnail(image_field='thumbnail')

    readonly_fields = ('slug_link', 'cover_image_tag', 'main_image_tag')

    search_fields = ('title', 'title_english', 'content', 'content_english')
    list_filter = ('pub_date', 'category')
    list_display = ('title', 'category', 'pub_date', 'article_link')


    def article_link(self, obj):
        return format_html(f'<a href="/blog/article/{obj.pk}/{obj.slug}" target="_blank">www.azermds.org/blog/article/{obj.pk}/{obj.slug}</a>')
    

    inlines = (ArticleImageInline,)
    


    


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'title_english', 'slug_link')
    readonly_fields = ('slug_link',)

    search_fields = ('title', 'title_english')
    list_display = ('title', 'category_link')

    def category_link(self, obj):
        return format_html(f'<a href="/blog/?type=category&value={obj.slug}&page=1" target="_blank">www.azermds.org/blog/?type=category&value={obj.slug}&page=1</a>')
    


admin.site.site_header = 'AZERMDS.ORG ADMİN PANELİ'