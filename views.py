from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

from .models import *


class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())


def classificacio_menu(request):
    queryset = Lliga.objects.all()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio', lliga.id)

    form = MenuForm()
    return render(request, "classificacio_menu.html", {
        "lligues": queryset,
        "form": form,
    })


def classificacio(request, lliga_id):
    lliga = Lliga.objects.get(pk=lliga_id)
    equips = lliga.equips.all()
    classi = []

    for equip in equips:
        punts = 0
        for partit in lliga.partits.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append((punts, equip.nom))
    classi.sort(reverse=True)
    return render(request, "classificacio.html", {
        "classificacio": classi,
    })


class EquipForm(forms.ModelForm):
    class Meta:
        model = Equip
        exclude = ()


def crea_equip(request):
    form = EquipForm()
    if request.method == "POST":
        form = EquipForm(request.POST)
        if form.is_valid():
            equips = Equip.objects.filter(nom=form.cleaned_data.get("nom"))
            if equips.count() > 0:
                return HttpResponse("ERROR: el nom de l'equip ja existeix.")
            form.save()
    return render(request, "crea_equip.html", {
        "form": form,
    })
