from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required
from .forms import RejestracjaForm, ListingForm
from django.contrib import messages

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

def register(request):
    if request.method == 'POST':
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto zostało utworzone! Możesz się zalogować.")
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RejestracjaForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('market:listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'market/create_listing.html', {'form': form})


@login_required
def kup_gre(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.is_sold:
        messages.error(request, "Ta gra została już sprzedana!")
        return redirect('market:listing_list')

    if listing.user == request.user:
        messages.warning(request, "Nie możesz kupić własnej oferty!")
        return redirect('market:listing_detail', pk=pk)

    if request.method == 'POST':
        listing.is_sold = True
        listing.save()

        messages.success(request, f"Gratulacje! Kupiłeś grę: {listing.game.title}")
        return redirect('market:listing_list')

    return redirect('market:listing_detail', pk=pk)