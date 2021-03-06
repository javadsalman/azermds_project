from django.views.generic import View, DetailView, ListView
from django.utils.translation import get_language
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from .models import Article, Category


printn = lambda *x: print('\n\n\n\n', *x, '\n\n\n\n')




class ArticleListView(DetailView):
    model = Article
    template_name = "article.html"
    context_object_name = 'article'


class BlogListView(ListView):
    template_name = "blog.html"
    paginate_by = 7
    context_object_name = 'articles'

    def get_queryset(self):
        query = self.request.GET
        type = query.get('type')
        if not type:
            articles = Article.objects.all()
        elif type == 'category':
            articles = self.category_filter(query['value'])
        elif type == 'date':
            articles = self.date_filter(query['value'])
        elif type == 'search':
            articles = self.search(query['category'], query['value'])
        else:
            articles = Article.objects.none()

        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = Category.objects.annotate(Count('article'))
        context.update({
            'categories': counts,
            'all_category_count': sum(map(lambda x: x.article__count, counts)),
            'page_list': self.get_page_list(context['page_obj'].number, context['page_obj'].paginator.num_pages, button_count=5   ),
        })
        return context

    # get pagination number list like google style. For example if the max page button count is 5 and current page is 7 but total page count is 8
    # then it gives 4, 5, 6, 7, 8. But most normal situation for example 20 total page and max 5 page count and current page 12...
    # then it gives a range with set 12 to center and add 2 to right and subtract 2 to right. It shows as 10, 11, 12, 13, 14
    def get_page_list(self, current_page, page_count, button_count):
        if page_count <= button_count:
            return list(range(1, page_count+1))
        else:
            start = current_page - button_count//2
            end = current_page + button_count//2
            print(start, end)
            if start < 1:
                end+= 1-start
                start = 1
            elif end > page_count:
                start-= end-page_count
                end = page_count
            return list(range(start, end+1))[:page_count]


    
    def category_filter(self, value):
        try:
            return Category.objects.get(slug = value).article_set.all()
        except ObjectDoesNotExist:
            return Article.objects.none()
    
    def date_filter(self, value):
        if value == 'today':
            selected_date = {'pub_date': timezone.now().date()}
        elif value == 'yesterday':
            selected_date = {'pub_date': timezone.now().date() - timedelta(1)}
        elif value == 'a_week_ago':
            selected_date = {'pub_date__lt': timezone.now().date() - timedelta(7), 'pub_date__gt': timezone.now().date() - timedelta(14)}
        elif value == 'a_month_ago':
            selected_date = {'pub_date__year': (timezone.now().date() - timedelta(31)).year, 'pub_date__month': (timezone.now().date() - timedelta(31)).month}
        elif value == 'a_year_ago':
            selected_date = {'pub_date__year': (timezone.now().date() - timedelta(365)).year}
        else:
            return Article.objects.none()
            
        return Article.objects.filter(**selected_date)

    def search(self, category, value):
        category_parameter = {'category': Category.objects.get(slug = category)} if category else {}
        vector = SearchVector('title') if get_language() == 'az' else SearchVector('title_english')
        return Article.objects.annotate(search=vector).filter(search__contains = value, **category_parameter)
    

         