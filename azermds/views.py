from django.views.generic import TemplateView
from app.blog.models import Category

class IndexView(TemplateView):
    template_name = "base/index/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Category.objects.raw( "SELECT * FROM blog_article WHERE category_id = (SELECT id FROM blog_category WHERE slug='yenilikler') ORDER BY pub_date DESC LIMIT 3 " )
        return context
    