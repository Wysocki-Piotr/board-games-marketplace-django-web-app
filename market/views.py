from django.shortcuts import render, get_object_or_404
from .models import Listing

# Create your views here.
def listing_list(request):
    # Pobieramy wszystkie oferty, które nie są sprzedane
    listings = Listing.objects.filter(is_sold=False)

    context = {
        'listings': listings
    }
    return render(request, 'market/listing_list.html', context)

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'market/listing_detail.html', {'listing': listing})