from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa kategorii")
    description = models.TextField(blank=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name

class BoardGame(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games', verbose_name="Kategoria")
    title = models.CharField(max_length=200, verbose_name="Tytuł gry")
    publisher = models.CharField(max_length=200, verbose_name="Wydawca", blank=True)
    description = models.TextField(verbose_name="Opis gry")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gra planszowa"
        verbose_name_plural = "Gry planszowe"

    def __str__(self):
        return self.title

# 3. Model Oferty (Konkretny egzemplarz sprzedawany przez usera)
class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Nowa (w folii)'),
        ('used_good', 'Używana (stan bdb)'),
        ('used_poor', 'Używana (widoczne ślady)'),
    ]

    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE, related_name='listings', verbose_name="Gra",
                             null=True, blank=True)
    custom_title = models.CharField(max_length=200, blank=True, verbose_name="Własny tytuł gry (jeśli brak na liście)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Sprzedający")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena (PLN)")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used_good', verbose_name="Stan")
    image = models.ImageField(upload_to='game_photos/', blank=True, null=True, verbose_name="Zdjęcie")
    is_sold = models.BooleanField(default=False, verbose_name="Sprzedane")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Oferta sprzedaży"
        verbose_name_plural = "Oferty sprzedaży"

    def __str__(self):
        title = self.game.title if self.game else self.custom_title
        return f"{title} - {self.price} zł ({self.user.username})"

    def get_title(self):
        return self.game.title if self.game else self.custom_title
