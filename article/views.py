from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from article.models import Article, Comment
from forms import ArticleForm, CommentForm
from django.utils import timezone
from django.core.context_processors import csrf



def articles(request):
    args = {}
    args['articles'] = Article.objects.all()
    args.update(csrf(request))
    return render_to_response('articles.html',
        args)

def article(request, article_id=1):
    return render_to_response('article.html',
        {'article':Article.objects.get(id=article_id)})


def create(request):
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/articles/all')
    else:
        form = ArticleForm()
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('create_article.html', args)

def like_article(request, article_id):
    if article_id:
        a = Article.objects.get(id=article_id)
        a.likes+=1
        a.save()
    return HttpResponseRedirect('/articles/get/%s'% article_id)


def add_comment(request, article_id):
    a = Article.objects.get(id=article_id)
    if request.method == 'POST':
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.pub_date = timezone.now()
            c.article = a
            c.save()
            return HttpResponseRedirect('/articles/get/%s'%article_id)
    else:
        f = CommentForm()
        args = {}
        args.update(csrf(request))
        args['article'] = a
        args['form'] = f
        return render_to_response('add_comment.html', args)

def search_titles(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ""

    articles = Article.objects.filter(title__contains=search_text)
    return render_to_response('ajax_search.html',
                                {'articles':articles})