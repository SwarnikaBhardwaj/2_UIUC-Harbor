# from django.shortcuts import render
#
#
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.views import View
# from django.views.generic import ListView
# from .models import Listing
#
# def listing_manual_view(request):
#    listings = Listing.objects.filter(is_active=True)
#
#
#    html = "<h1>Collective Circle Listings</h1>"
#    for listing in listings:
#        html += f"""
#            <div>
#                <h3>{listing.title}</h3>
#                <p>Category: {listing.category.name}</p>
#                <p>Seller: {listing.seller.first_name}</p>
#            </div>
#            <hr>
#        """
#
#
#    return HttpResponse(html)
#
# def listing_render_view(request):
#    listings = Listing.objects.filter(is_active=True)
#    return render(
#        request,
#        "listings/listing_features.html",
#        {"listings": listings}
#    )
#
# class ListingBaseCBV(View):
# def get(self, request):
#        listings = Listing.objects.filter(is_active=True)
#        return render(
#            request,
#            "listings/listing_features.html",
#            {"listings": listings}
#        )
#
# class ListingGenericCBV(ListView):
#    model = Listing
#    template_name = "listings/listing_features.html"
#    context_object_name = "listings"
#
#     def get_queryset(self):
#         return Listing.objects.filter(is_active=True)
#

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from django.db.models import Count, F
from .models import Listing, Student
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Student, Category
import json, requests, csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




def listing_manual_view(request):
    listings = Listing.objects.filter(is_active=True)
    html = "<h1>Collective Circle Listings</h1>"
    for listing in listings:
        html += f"""
            <div>
                <h3>{listing.title}</h3>
                <p>Category: {listing.category.name}</p>
                <p>Seller: {listing.seller.first_name}</p>
            </div>
            <hr>
        """
    return HttpResponse(html)

@login_required
def listing_render_view(request):
    listings = Listing.objects.filter(is_active=True)
    return render(
        request,
        "listings/listing_features.html",
        {"listings": listings}
    )


class ListingBaseCBV(View):
    def get(self, request): # Fixed Indentation
        listings = Listing.objects.filter(is_active=True)
        return render(
            request,
            "listings/listing_features.html",
            {"listings": listings})


class ListingGenericCBV(ListView):
    model = Listing
    template_name = "listings/listing_features.html"
    context_object_name = "listings"

    def get_queryset(self): # Fixed Indentation
        return Listing.objects.filter(is_active=True)

# started here in week 3: Swarnika's part

def home_view(request):
    total_listings = Listing.objects.filter(is_active=True).count()
    total_students = Student.objects.filter(is_verified=True).count()
    total_categories = Category.objects.count()
    context = {
        'total_listings': total_listings,
        'total_students': total_students,
        'total_categories': total_categories,
    }
    return render(request, 'listings/home.html', context)


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'listings/student_detail.html'
    context_object_name = 'student'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_listings'] = self.object.listings.filter(is_active=True)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'listings/category_detail.html'
    context_object_name = 'category'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_listings'] = self.object.listings.filter(is_active=True)
        return context

class StudentListView(ListView):
    model = Student
    template_name = 'listings/student_list.html'
    context_object_name = 'students'
    def get_queryset(self):
        return Student.objects.filter(is_verified=True)


class CategoryListView(ListView):
    model = Category
    template_name = 'listings/category_list.html'
    context_object_name = 'categories'


class ListingFilterCBV(ListView):
    model = Listing
    template_name = 'listings/listing_filter.html'
    context_object_name = 'listings'

    def get_queryset(self):
        return Listing.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):
        min_price = request.POST.get('min_price', '')
        max_price = request.POST.get('max_price', '')

        listings = Listing.objects.filter(is_active=True)
        if min_price:
            listings = listings.filter(price__gte=float(min_price))
        if max_price:
            listings = listings.filter(price__lte=float(max_price))

        return render(request, self.template_name, {
            'listings': listings,
            'min_price': min_price,
            'max_price': max_price,
            'search_type': 'POST (CBV Implementation)'
        })

def listing_search_get(request):
    query = request.GET.get('q', '')
    if query:
        listings = Listing.objects.filter(
            is_active=True,
            title__icontains=query
        ) | Listing.objects.filter(
            is_active=True,
            description__icontains=query
        )
    else:
        listings = Listing.objects.filter(is_active=True)
    context = {
        'listings': listings,
        'query': query,
        'search_type': 'GET'
    }
    return render(request, 'listings/listing_search.html', context)


# def listing_search_post(request):
#     listings = Listing.objects.filter(is_active=True)
#     min_price = None
#     max_price = None
#     if request.method == 'POST':
#         min_price = request.POST.get('min_price', '')
#         max_price = request.POST.get('max_price', '')
#         if min_price:
#             listings = listings.filter(price__gte=float(min_price))
#         if max_price:
#             listings = listings.filter(price__lte=float(max_price))
#
#     context = {
#         'listings': listings,
#         'min_price': min_price,
#         'max_price': max_price,
#         'search_type': 'POST'
#     }
#     return render(request, 'listings/listing_filter.html', context)


def listing_by_category_name(request, category_name):
    listings = Listing.objects.filter(
        is_active=True,
        category__name__iexact=category_name
    )
    context = {
        'listings': listings,
        'category_name': category_name,
        'count': listings.count()
    }
    return render(request, 'listings/listing_by_category.html', context)


def aggregation_stats(request):
    from django.db.models import Count
    total_listings = Listing.objects.filter(is_active=True).count()
    total_students = Student.objects.count()
    categories_with_counts = Category.objects.annotate(
        listing_count=Count('listings')
    ).order_by('-listing_count')
    students_with_counts = Student.objects.annotate(
        listing_count=Count('listings')
    ).filter(listing_count__gt=0).order_by('-listing_count')
    context = {
        'total_listings': total_listings,
        'total_students': total_students,
        'categories_with_counts': categories_with_counts,
        'students_with_counts': students_with_counts,
    }
    return render(request, 'listings/aggregation_stats.html', context)

def listing_api_list(request):
    listings = Listing.objects.filter(is_active=True)
    category_name = request.GET.get('cat')
    if category_name:
        listings = listings.filter(category__name__icontains=category_name)
    data = []
    for item in listings:
        data.append({
            "title": item.title,
            "price": str(item.price) if item.price else "Free",
            "category": item.category.name,
            "seller": item.seller.first_name
        })
    return JsonResponse({"listings": data, "count": len(data)}, safe=False)

def listings_per_category_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)
    data = (
        Listing.objects
        .filter(is_active=True)
        .values(category_name=F("category__name"))
        .annotate(listing_count=Count("id"))
        .order_by("category_name")
    )
    response =  JsonResponse(list(data), safe=False)
    # 3.2
    response["Access-Control-Allow-Origin"] = "https://vega.github.io"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type"
    return response

def api_mime_demo(request):
    sample_data = {"message": "Hello, this is a MIME test"}
    if request.GET.get('type') == 'http':
        return HttpResponse(json.dumps(sample_data))
    return JsonResponse(sample_data)

def category_chart_view(request):
    return render(request, "listings/category_chart.html")

from django.db.models import Avg, F

def listings_avg_price_per_category_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)
    data = (
        Listing.objects.filter(is_active=True, price__isnull=False)
        .values(category_name=F("category__name"))
        .annotate(avg_price=Avg("price"))
        .order_by("category_name")
    )
    data_list = [
        {"category_name": d["category_name"], "avg_price": float(d["avg_price"])}
        for d in data
    ]
    return JsonResponse(data_list, safe=False)

def price_line_chart_view(request):
    return render(request, "listings/price_line_chart.html")

@login_required
def external_api_demo(request):
    name = request.GET.get("name", "")
    if not name:
        return JsonResponse({"error": "Please provide a 'name' parameter"}, status=400)
    try:
        response = requests.get(
            "https://api.agify.io",
            params={"name": name},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    result = {
        "query_name": name,
        "predicted_age": data.get("age"),
        "count_of_listings": Listing.objects.filter(seller__first_name__iexact=name).count()
    }
    return JsonResponse(result)

def export_students_csv(request):
    now = timezone.now()
    filename = f"students_{now.strftime('%Y-%m-%d_%H-%M')}.csv"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Verified', 'Created At'])
    for student in Student.objects.all().order_by('first_name'):
        writer.writerow([
            student.first_name,
            student.last_name,
            student.university_email,
            student.is_verified,
            student.created_at,
        ])
    return response

def export_students_json(request):
    now = timezone.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"students_{now}.json"
    students_qs = Student.objects.all().order_by('id')
    students_list = [
        {
            "id": s.id,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "email": s.university_email,
            "is_verified": s.is_verified
        }
        for s in students_qs
    ]
    data = {
        "generated_at": timezone.now().isoformat(),
        "record_count": students_qs.count(),
        "students": students_list
    }

    response = JsonResponse(data, json_dumps_params={"indent": 2})
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

def reports_view(request):
    total_students = Student.objects.count()
    verified_students = Student.objects.filter(is_verified=True).count()
    students_by_verified = Student.objects.values('is_verified').annotate(count=Count('id'))
    students_dict = {str(item['is_verified']): item['count'] for item in students_by_verified}
    context = {
        "total_students": total_students,
        "verified_students": verified_students,
        "students_by_verified": students_dict
    }
    return render(request, "listings/reports.html", context)

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})