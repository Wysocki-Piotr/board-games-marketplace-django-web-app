from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing
from django.contrib.auth.decorators import login_required
from .forms import RejestracjaForm, ListingForm
from django.contrib import messages
from django.http import JsonResponse

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

        if listing.game:
            game_title = listing.game.title
        else:
            game_title = listing.custom_title

        messages.success(request, f"Gratulacje! Kupiłeś grę: {game_title}")

        messages.success(request, f"Gratulacje! Kupiłeś grę: {listing.game.title}")
        return redirect('market:listing_list')

    return redirect('market:listing_detail', pk=pk)


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.user != request.user:
        messages.error(request, "Nie możesz edytować cudzej oferty!")
        return redirect('market:listing_detail', pk=pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Ogłoszenie zostało zaktualizowane!")
            return redirect('market:listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)

    # Używamy tego samego szablonu co przy tworzeniu, ale przekazujemy flagę 'is_edit'
    return render(request, 'market/create_listing.html', {
        'form': form,
        'title': 'Edytuj ogłoszenie'
    })


def search_listings(request):
    query = request.GET.get('query', '')
    max_price = request.GET.get('max_price')
    condition = request.GET.get('condition')

    listings = Listing.objects.filter(is_sold=False)

    if query:
        from django.db.models import Q
        listings = listings.filter(
            Q(game__title__icontains=query) |
            Q(custom_title__icontains=query)
        )

    if max_price:
        listings = listings.filter(price__lte=max_price)

    if condition and condition != 'all':
        listings = listings.filter(condition=condition)

    data = []
    for item in listings:
        title = item.game.title if item.game else item.custom_title
        category = item.game.category.name if item.game else "Inne"

        image_url = item.image.url if item.image else ""

        data.append({
            'id': item.id,
            'title': title,
            'category': category,
            'price': str(item.price),
            'condition_display': item.get_condition_display(),
            'image_url': image_url,
            'seller': item.user.username
        })

    return JsonResponse({'listings': data})