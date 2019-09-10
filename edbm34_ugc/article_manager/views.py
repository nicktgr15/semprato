import joblib
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from article_manager.models import Article, Category, ArticleTag, BlockedTerm
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import ArticleForm
from PIL import Image, ExifTags
import exifread as ef
import re
from datetime import datetime

def category(request, category_name):
    c = Category.objects.filter(slug=category_name)[0]
    context = {'all_articles': c.article_category.all().exclude(publish=False), 'category': c}

    return render(request, 'article_manager/category.html', context)


def article(request, category_name, article_id):
    try:
        article = Article.objects.filter(id=article_id)[0]
        # article.hits += 1
        # article.save()
        pass
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'article_manager/article.html', {'article': article, 'category_name': category_name})


def home(request):
    all_articles = Article.objects.all().order_by('-created_at').exclude(publish=False)
    # print(all_articles[0].category)
    context = {'all_articles': all_articles}
    return render(request, 'article_manager/home.html', context)


# def post_article_step_2(request):
#
#     if request.method == 'POST':
#
#         form = ArticleForm(request.POST)
#
#         if form.is_valid():
#             category = Category.objects.get(pk=request.POST.get('category'))
#
#             article = Article.objects.create(
#                 category=category,
#                 text=request.POST.get('text'),
#                 title=request.POST.get('title'),
#             )
#             article.save()
#
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return redirect(reverse("article_manager:category", kwargs={'category_name': category.slug}))
#         else:
#             print("form not valid")
#     else:
#         old_post = request.session.get('post_data')
#
#         count_vect = joblib.load("article_manager/nlp_models/count_vect.pkl")
#         tfidf_transformer = joblib.load("article_manager/nlp_models/tfidf_transformer.pkl")
#         clf = joblib.load("article_manager/nlp_models/clf.pkl")
#         le = joblib.load("article_manager/nlp_models/label_encoder.pkl")
#
#         out_count = count_vect.transform([old_post['text']])
#         out = tfidf_transformer.transform(out_count)
#
#         category_number = clf.predict(out)[0]
#         category_name = le.classes_[category_number]
#         category = Category.objects.get(slug=category_name)
#
#         old_post["category"] = category.pk
#
#         form = ArticleForm(old_post)
#
#         return render(request, 'article_manager/article_post_step_2.html', {
#             'form': form,
#             'text': old_post['text'],
#             'title': old_post['title']
#         })


@login_required
def post_like_article(request, category_slug, article_id):
    article = Article.objects.get(pk=article_id)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    article.save()
    return redirect(
        reverse("article_manager:article", kwargs={'category_name': category_slug, 'article_id': article_id})
    )


def infer_category(input_text):
    count_vect = joblib.load("article_manager/nlp_models/count_vect.pkl")
    tfidf_transformer = joblib.load("article_manager/nlp_models/tfidf_transformer.pkl")
    clf = joblib.load("article_manager/nlp_models/clf.pkl")
    le = joblib.load("article_manager/nlp_models/label_encoder.pkl")

    out_count = count_vect.transform([input_text])
    out = tfidf_transformer.transform(out_count)

    category_number = clf.predict(out)[0]
    category_name = le.classes_[category_number]
    inferred_category = Category.objects.get(slug=category_name)
    return inferred_category


def extract_exif(img_path):
    try:
        img = Image.open(img_path)
        exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
        return exif
    except:
        return {}


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def getGPS(filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'latitude': lat_value, 'longitude': lon_value}
    return {}


@login_required
def post_article(request):
    if request.method == 'POST':

        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            category = Category.objects.get(pk=request.POST.get('category'))

            article = Article.objects.create(
                category=category,
                inferred_category=infer_category(request.POST.get('text')),
                text=request.POST.get('text'),
                title=request.POST.get('title'),
                author=request.user
            )

            terms = [term.name for term in BlockedTerm.objects.all()]
            for term in terms:

                found_terms = re.findall(r"[\s.,?;]+%s[\s.,?;]+" % term, article.text)
                found_terms = list(set([f.strip(" .,?;") for f in found_terms]))

                for f in found_terms:
                    article.text = article.text.replace(term, '<span style="background-color:#f1c40f">%s</span>' % term)
                    article.contains_blocked_terms = True

            if 'image1' in request.FILES:
                article.image1 = request.FILES['image1']

            if 'image2' in request.FILES:
                article.image2 = request.FILES['image2']

            if 'image3' in request.FILES:
                article.image3 = request.FILES['image3']

            tags = request.POST.get('tags').split(",")

            for tag in tags:
                try:
                    article_tag = ArticleTag.objects.get(name=tag)
                except ArticleTag.DoesNotExist:
                    article_tag = ArticleTag.objects.create(
                        name=tag
                    )
                    article_tag.save()

                article.tags.add(article_tag)

            article.save()

            if 'image1' in request.FILES:
                exif1 = extract_exif(article.image1.path)
                gps = getGPS(article.image1.path)

                parsed_date_1 = exif1.get("DateTime", "")
                if parsed_date_1 != "":
                    # 2010:05:16 23:35:03
                    article.image1_exif_datetime = datetime.strptime(parsed_date_1, "%Y:%m:%d %H:%M:%S")

                    diff_days = (datetime.now() - article.image1_exif_datetime).days
                    if diff_days > 60 or diff_days < 0:
                        article.irregular_image_date = True

                print(article.image1_exif_datetime)
                article.image1_location = "%s,%s" % (gps.get('latitude', ""), gps.get('longitude', ""))

            if 'image2' in request.FILES:
                exif2 = extract_exif(article.image2.path)
                gps = getGPS(article.image2.path)

                parsed_date_2 = exif2.get("DateTime", "")
                if parsed_date_2 != "":
                    # 2010:05:16 23:35:03
                    article.image2_exif_datetime = datetime.strptime(parsed_date_2, "%Y:%m:%d %H:%M:%S")

                    diff_days = (datetime.now() - article.image2_exif_datetime).days
                    if diff_days > 60 or diff_days < 0:
                        article.irregular_image_date = True

                print(article.image2_exif_datetime)
                article.image2_location = "%s,%s" % (gps.get('latitude', ""), gps.get('longitude', ""))

            if 'image3' in request.FILES:
                exif3 = extract_exif(article.image3.path)
                gps = getGPS(article.image3.path)

                parsed_date_3 = exif3.get("DateTime", "")
                if parsed_date_3 != "":
                    # 2010:05:16 23:35:03
                    article.image3_exif_datetime = datetime.strptime(parsed_date_3, "%Y:%m:%d %H:%M:%S")

                    diff_days = (datetime.now() - article.image3_exif_datetime).days
                    if diff_days > 60 or diff_days < 0:
                        article.irregular_image_date = True

                print(article.image3_exif_datetime)
                article.image3_location = "%s,%s" % (gps.get('latitude', ""), gps.get('longitude', ""))

            article.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect(reverse("article_manager:home"))
        else:
            print("form not valid")

        # create a form instance and populate it with data from the request:
        # form = ArticleForm(request.POST)
        # # check whether it's valid:
        #
        # if request.POST.get('text') != "" and request.POST.get('title') != "":
        #     request.session['post_data'] = request.POST
        #     return redirect(reverse("article_manager:post_article_step_2"))
        # else:
        #     print("Title and Text not provided")

    else:
        form = ArticleForm()
        return render(request, 'article_manager/article_post.html', {'form': form})
