from django.db import models
from django.db.models.constraints import UniqueConstraint
from datetime import datetime


class BaseModelWithDateStamp(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    version_number = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.version_number += 1
        super().save(*args, **kwargs)


class Friend(BaseModelWithDateStamp):
    name = models.CharField(
        max_length=100,
        verbose_name="Friend name",
        help_text="Enter your friend's name.",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Phone Number",
        help_text="Enter the contact's phone number.",
    )

    def __str__(self):
        return self.name

    class Meta:
        """
        A Meta egy belső osztály Django modellekben, ami nem mezőket definiál,
        hanem a modell viselkedését és adatbázissal kapcsolatos beállításokat szabályoz.

        Code-first:
        A managed = True esetén a Django migrációkon keresztül automatikusan kezeli az adatbázistáblát
        (létrehozás, módosítás). A modell definíciója vezérli az adatbázis szerkezetét.
        Database-first:
        A managed = False a database-first irányt támogatja,
        amikor az adatbázis már létezik, és Django csak olvassa, de nem változtatja a táblákat.
        """

        managed = True  # Django kezeli a táblát (létrehozza/módosítja migrációkkal)
        db_table = "main_friend"  # Az adatbázisban használt tábla neve (alapértelmezett helyett)
        verbose_name = "Friend"  # Egyes számú megjelenítendő név (pl. admin felületen)
        verbose_name_plural = "Friends"  # Többes számú megjelenítendő név
        ordering = [
            "id"
        ]  # Alapértelmezett rendezés lekérdezéseknél (itt az id szerint növekvő)
        app_label = "main"  # Ha a modell nincs a szokásos helyen, ezt használja az app azonosítására
        constraints = [
            UniqueConstraint(
                fields=["name", "phone"], name="unique_phone_name_combination"
            )
        ]
