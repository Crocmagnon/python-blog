from articles.models import Article, Page


def pages(request):
    return {"pages": Page.objects.filter(status=Article.PUBLISHED)}
