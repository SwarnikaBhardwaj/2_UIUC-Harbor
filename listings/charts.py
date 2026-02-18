import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.db.models import Count
from .models import Category
def marketplace_distribution_chart(request):
    data = Category.objects.annotate(
        item_count=Count('listings')
    ).filter(item_count__gt=0).order_by('-item_count')
    labels = [cat.name for cat in data]
    counts = [cat.item_count for cat in data]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, counts, color='teal')
    ax.set_title('Listing Volume by Category')
    ax.set_xlabel('Category Name')
    ax.set_ylabel('Total Listings')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')