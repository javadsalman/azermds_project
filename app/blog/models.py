from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField, ImageSpecField
from django.utils.html import format_html

printn = lambda x: print(f'\n\n\n\n{x}\n\n\n\n')

def get_slug(slug):
    return slugify(slug.lower().translate(str.maketrans('üöğıəçş', 'uogiecs')))


class Category(models.Model):
    title = models.CharField(max_length = 50, unique = True, null=False, verbose_name = 'Azərbaycanca Başlıq *')
    title_english = models.CharField(max_length = 50, unique = True, verbose_name = 'İngiliscə Başlıq')
    slug = models.SlugField(unique=True, default='', blank=True, verbose_name = 'Link')

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_title(self):
        return self.title if get_language() == 'az' or not self.title_english else self.title_english
    
    def slug_link(self):
        if self.slug:
            return format_html(u'<a href="/blog/?type=category&value={0}&page=1" target="_blank">www.azermds.org/blog/?type=category&value={0}&page=1</a>'.format(self.slug))
        else:
            return '-'
    slug_link.short_description = 'Link'
    slug_link.allow_tags = True

class Article(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length = 100, verbose_name = 'Azərbaycanca Başlıq *')
    title_english = models.CharField(max_length = 100, verbose_name = 'İngiliscə Başlıq', null=True, blank=True)
    content = RichTextField(
        null=False,
        verbose_name='Azərbaycanca Kontent *',
        # CKEDITOR.config.extraPlugins:
        extra_plugins=['youtube'],
        # CKEDITOR.plugins.addExternal(...)
        external_plugin_resources=[(
            'youtube',
            '/staticfiles/ckeditor/extension/youtube/',
            'plugin.js',
        )],
    )
    content_english = RichTextField(
        verbose_name='Ingiliscə Kontent',
        extra_plugins=['youtube'],
        null = True,
        blank=True,
        external_plugin_resources=[(
            'youtube',
            '/staticfiles/ckeditor/extension/youtube/',
            'plugin.js',
        )],
        )
    slug = models.SlugField(default='', blank=True, verbose_name = 'Link')
    cover_image = ProcessedImageField(upload_to = 'article/cover/', options={'quality': 150}, blank=True, null=True, verbose_name = 'Qapaq Şəkli', format='JPEG')
    main_image = ProcessedImageField(upload_to = 'article/main_images', options={'quality': 90}, null=False, verbose_name = 'Əsas şəkil *', format='JPEG')
    thumbnail = ImageSpecField(source = 'main_image', format='JPEG', options={'quality':60})
    category = models.ForeignKey(Category, null=False, on_delete = models.PROTECT, verbose_name = 'Kateqoriya *')
    pub_date = models.DateTimeField(auto_now_add = True, verbose_name = 'Paylaşılma Tarixi')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title

    def cover_image_tag(self):
        return format_html(u'<img src="{}" width="200"/>'.format(self.cover_image.url))
    cover_image_tag.short_description = 'Mövcud qapaq şəkli'
    cover_image_tag.allow_tags = True

    def main_image_tag(self):
        return format_html(u'<img src="{}" width="200"/>'.format(self.main_image.url))
    main_image_tag.short_description = 'Mövcud Əsas şəkil'
    main_image_tag.allow_tags = True

    def slug_link(self):
        if self.slug:
            return format_html(u'<a href="/blog/article/{1}/{0}" target="_blank">www.azermds.org/blog/article/{1}/{0}</a>'.format(self.slug, self.pk))
        else:
            return '-'
    slug_link.short_description = 'Link'
    slug_link.allow_tags = True

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_title(self):
        return self.title if get_language() == 'az' or not self.title_english else self.title_english
    
    def get_content(self):
        return self.content if get_language() == 'az' or not self.content_english else self.content_english   



class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='article/images/', options={'quality': 90}, verbose_name='Şəkil', format='JPEG')

    def image_tag(self):
        return format_html(u'<img src="{}" width="150"/>'.format(self.image.url))
    image_tag.short_description = 'Mövcud şəkil'
    image_tag.allow_tags = True

    

    
