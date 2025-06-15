from django.contrib import admin

from .models import Lliga, Equip, Jugador, Partit, Event

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps", "tipus", "jugador", "equip"]
    ordering = ("temps",)

class PartitAdmin(admin.ModelAdmin):
    search_fields = ["local__nom", "visitant__nom", "lliga__nom"]
    readonly_fields = ["resultat",]
    list_display = ["local", "visitant", "resultat", "lliga", "data"]
    ordering = ("-data",)
    inlines = [EventInline,]

    def resultat(self, obj):
        gols_local = obj.events.filter(
            tipus="GOL",
            equip=obj.local).count()
        gols_visit = obj.events.filter(
            tipus="GOL",
            equip=obj.visitant).count()
        return "{} - {}".format(gols_local, gols_visit)

admin.site.register(Partit, PartitAdmin)
