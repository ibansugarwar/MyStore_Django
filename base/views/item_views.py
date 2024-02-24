from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag
from django.shortcuts import redirect
from django.shortcuts import render

class IndexListView(ListView):
    model = Item
    template_name = 'pages/index.html'
    queryset = Item.objects.filter(is_published=True)


class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item.html'

# カテゴリ一覧からカテゴリを選択した際の処理
class CategoryListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 24

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        category = Item.objects.filter(is_published=True, category=self.category)
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_name"] = self.category.name
        return context


class TagListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 2

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.tag.name
        return context


class SearchListView(ListView):
    model = Item

    def get(self, request):
        search_keyword = request.GET.get('search_keyword')
        target_word = search_keyword.strip()

        if isValidate(target_word):
            # キーワードが空の場合は商品リストを再取得
            object_list = Item.objects.all()
            searched_flg = False
        else:
            object_list = Item.objects.filter(is_published=True, name__contains=target_word)
            searched_flg = True
        
        if object_list.count() == 0:
            # 検索結果が存在しない場合
            object_count = 0
        else:
            object_count = object_list.count()


        context = {
            'object_list': object_list,
            'object_count': object_count,
            'search_keyword': target_word,
            'searched_flg': searched_flg
        }
        return render(request, 'pages/index.html', context)


# null・空文字の場合はTrueを返却
def isValidate(str):
    if len(str) == 0 :
        return True
    else:
        return False