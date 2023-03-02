from django.shortcuts import render, redirect
from . import util
from django import forms
from random import randint
import markdown2

class NewArticleForm(forms.Form):
    title = forms.CharField(label="Title", max_length=25, required=True)
    content = forms.CharField(widget=forms.Textarea, label=False)

class EditArticleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label=False)


def index(request):
    entries = ["There is no articles yet"]
    if util.list_entries():
        entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "articles": entries
    })

def wiki(request, title):
    page = "encyclopedia/not_found.html"
    content = markdown2.markdown(util.get_entry(title))
    if content:
        page = "encyclopedia/article.html"
    return render(request, page, {
        "title": title,
        "article": content
    })

def search(request):
    response = redirect("/")
    if request.method == "GET" and  'q' in request.GET:
        request_word = request.GET['q'].lower()
        filtered_entries = []
        for entry in util.list_entries():
            if entry.lower().__contains__(request_word) and len(entry.lower()) == len(request_word):
                response = redirect(f"/wiki/{entry}")
                break
            elif entry.lower().__contains__(request_word):
                filtered_entries.append(entry)
            if not filtered_entries: 
                response = render(request,  "encyclopedia/not_found.html", {"title": request_word})
            else:
                response = render(request, "encyclopedia/index.html", {
                    "articles": filtered_entries
                })
    return response

def add_article(request):
    file_exist_error = ""
    if request.method == "POST":
        form = NewArticleForm(request.POST)        
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]
            if util.save_entry(title, content):
                file_exist_error = "This article is already exist!"                            
        if not form.is_valid() or file_exist_error:
           return render(request, "encyclopedia/new.html", {
            "new_form": form,
            "error": file_exist_error
            }) 
        else:
            return redirect(f"/wiki/{title}")

    return render(request, "encyclopedia/new.html", {
        "new_form": NewArticleForm(),
        "error": file_exist_error
    })

def edit_article(request, title):
    content = util.get_entry(title)
    page = "encyclopedia/not_found.html"
    edit_data = {"title": title}
    if content:
        form = EditArticleForm({"content": content})
        page = "encyclopedia/edit.html"
        edit_data.update({
            "new_form": form,
            "error": ""          
        })
    if request.method == "POST":
        form = EditArticleForm(request.POST) 
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content, True)
            return redirect(f"/wiki/{title}")
    return render(request, page, edit_data)

def random_article(request):
    articles = util.list_entries()
    articles_count = len(articles)-1
    article_index = randint(0, articles_count)
    return redirect(f"/wiki/{articles[article_index]}")