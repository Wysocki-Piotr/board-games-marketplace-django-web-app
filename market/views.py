from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing, Offer
from django.contrib.auth.decorators import login_required
from .forms import RejestracjaForm, ListingForm
from django.contrib import messages
from django.http import JsonResponse
from .serializers import ListingSerializer, OfferSerializer
from .filters import ListingFilter
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status as http_status
from django.db.models import Q

# Create your views here.
def listing_list(request):
    listings = Listing.objects.filter(is_sold=False).order_by('-created_at')

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

    return render(request, 'market/create_listing.html', {
        'form': form,
        'title': 'Edytuj ogłoszenie'
    })


class ListingSearchAPIView(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):

        queryset = Listing.objects.filter(is_sold=False).select_related('game', 'game__category', 'user')

        query = self.request.query_params.get('query')
        max_price = self.request.query_params.get('max_price')
        condition = self.request.query_params.get('condition')

        if query:
            queryset = queryset.filter(
                Q(game__title__icontains=query) |
                Q(custom_title__icontains=query)
            )

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if condition and condition != 'all':
            queryset = queryset.filter(condition=condition)

        return queryset.order_by('-created_at')

class CreateOfferAPIView(generics.CreateAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class ManageOfferAPIView(generics.RetrieveUpdateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        offer = self.get_object()

        if offer.listing.user != request.user:
            return Response(
                {"error": "Nie jesteś właścicielem tego ogłoszenia!"},
                status=http_status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")

        if new_status not in ['accepted', 'rejected']:
            return Response({"error": "Nieprawidłowy status."}, status=http_status.HTTP_400_BAD_REQUEST)

        if new_status == 'accepted':
            offer.listing.price = offer.price
            offer.listing.save()

        offer.status = new_status
        offer.save()

        return Response({"message": f"Oferta została {new_status}", "new_price": offer.listing.price})