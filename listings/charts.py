import matplotlib
matplotlib.use('Agg')  # MUST be called before importing pyplot
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.db.models import Count
from .models import Category
def marketplace_distribution_chart(request):
    # ORM Aggregation
    # Uses .annotate to group listings by category and count them
    # 'listings' refers to the related_name on your Listing model
    data = Category.objects.annotate(
        item_count=Count('listings')
    ).filter(item_count__gt=0).order_by('-item_count')

    # Unpack data for Matplotlib
    # Using list comprehension as shown in your sample code
    labels = [cat.name for cat in data]
    counts = [cat.item_count for cat in data]

    # Make chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, counts, color='teal')

    ax.set_title('Listing Volume by Category')
    ax.set_xlabel('Category Name')
    ax.set_ylabel('Total Listings')

    # Memory Awareness & Image Endpoint (Section 4 Requirement)
    # Use BytesIO to keep the image in RAM instead of writing to disk
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)  # Essential for memory management
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')