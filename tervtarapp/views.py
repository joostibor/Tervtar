from tervtarapp.models import Egyseg, Dokumentumtipus, Allomas, Vonal
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from tervtarapp.forms import AllomasAddForm, VonalAddForm, MyPwdChForm, MyAuthForm, SearchForm
from pathlib import Path

def homePageView(request):
    egysegek = [(e) for e in Egyseg.objects.all()]
    dokumentumok = [(d) for d in Dokumentumtipus.objects.all()]
    context = {
        'egysegek': egysegek,
        'dokumentumok': dokumentumok,
    }
    return render(request, 'homepage.html', context)

def signin(request):
    if request.method == "POST":
        form = MyAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Hibás felhasználónév vagy jelszó.")
        else:
            messages.error(request, "Hibás felhasználónév vagy jelszó.")
    form = MyAuthForm()
    return render (request=request, template_name="signin.html", context={"login_form":form})

def logout_req(request):
    logout(request)
    return redirect("/bejelentkezes")

def charchange(allomas):
    anev = list(allomas)
    anev[allomas.find('_')] = '-'
    allomas = ''.join(anev)
    return allomas


def folderlist(request):
    file = '/home/joost/Ttar/tervtar/tervtarapp/treefull.txt'
    folderstruct = []
    blacklist = ["Thumbs.db", "lista01.html", "lista02_nolinks.html", ".lnk", ".log", ".err", "(üres)"]
    form = SearchForm(request.POST)
    if form.is_valid():
        allomasnev = form.cleaned_data['allomas']
        if '_' in allomasnev:
            allomasnev = charchange(allomasnev)
        allomaskoz = form.cleaned_data['allomaskoz']
        vonal = form.cleaned_data['vonal']+".vonal"
        if vonal == '30.vonal':
            vonal = '30b.vonal'
        egyseg = form.cleaned_data['egyseg']
        dokumentum = form.cleaned_data['dokumentum']
        szelvenyszam = form.cleaned_data['szelvenyszam']

        kallomas = ''
        vallomas = ''
        if allomaskoz != '':
            kallomas = allomaskoz.partition('-')[0]
            vallomas = allomaskoz.partition('-')[2]
        if szelvenyszam != '' and szelvenyszam.count("-") == 1:
            kszelveny = int(szelvenyszam.partition('-')[0])
            vszelveny = int(szelvenyszam.partition('-')[2])
        elif szelvenyszam != '' and szelvenyszam.count("-") == 0:
            kszelveny = int(szelvenyszam.partition('-')[0])
            vszelveny = 0
        else:
            kszelveny = 0
            vszelveny = 0

        allomasok = [(a.allomasnev) for a in Allomas.objects.all()]
        for v in Vonal.objects.all():
            allomasok.append(v.kezdo_allomas)
            allomasok.append(v.vegallomas)
        vonalak = [(v.vonalszam + ".vonal") for v in Vonal.objects.all()]

        if allomasnev != '' and allomasnev not in allomasok:
            messages.error(request, "Az állomásnév nem szerepel az állomáslistában.")
            return redirect("/")

        if vonal != '.vonal' and vonal not in vonalak and vonal != '30b.vonal':
            messages.error(request, "A vonalszám nem szerepel a vonalak között.")
            return redirect("/")

        if szelvenyszam != '' and vonal == '.vonal':
            messages.error(request, "Szelvényszámhoz kötelező a vonal megadása.")
            return redirect("/")
            
        f = open(file, 'r')
        for line in f:
            black = False
            startpos = line.find('.')
            line = line[startpos:]
            for b in blacklist:
                if b in str(line):
                    black = True
            if black == False:
                if (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, True, True, True, True, True):
                    if allomasnev in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, False, True, True, True, True):
                    if vonal in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, True, False, True, True, True):
                    if egyseg in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, True, True, False, True, True):
                    if dokumentum in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, False, True, True, True, True):
                    if vonal in line and allomasnev in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, True, False, True, True, True):
                    if egyseg in line and allomasnev in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, True, True, False, True, True):
                    if dokumentum in line and allomasnev in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, False, False, True, True, True):
                    if vonal in line and egyseg in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, False, True, False, True, True):
                    if vonal in line and dokumentum in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, True, False, False, True, True):
                    if egyseg in line and dokumentum in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, False, False, True, True, True):
                    if vonal in line and allomasnev in line and egyseg in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, False, True, False, True, True):
                    if vonal in line and allomasnev in line and dokumentum in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, False, False, False, True, True):
                    if vonal in line and dokumentum in line and egyseg in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, True, False, False, True, True):
                    if dokumentum in line and allomasnev in line and egyseg in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (False, False, False, False, True, True):
                    if dokumentum in line and allomasnev in line and egyseg in line and vonal in line:
                        line = Path(line)
                        folderstruct.append(line)
                elif (allomasnev == '', vonal == '.vonal', egyseg == '', dokumentum == '', allomaskoz == '', szelvenyszam == '') == (True, False, True, True, True, False):
                    if line.count("+",line.rfind("/")) == 2 and vonal in line:
                        try:
                            fajlszelkezd = int(line[line.rfind("/")+1:line.find("+")])
                            fajlszelveg = int(line[line.rfind("-")+1:line.rfind("+")])
                            if vszelveny != 0:
                                if (fajlszelkezd <= kszelveny and fajlszelveg > kszelveny) or (fajlszelkezd < vszelveny and fajlszelveg < vszelveny and fajlszelveg > kszelveny) or (fajlszelkezd < vszelveny and fajlszelveg >= vszelveny):
                                    line = Path(line)
                                    folderstruct.append(line)
                            else:
                                if (fajlszelkezd <= kszelveny and fajlszelveg >= kszelveny):
                                    line = Path(line)
                                    folderstruct.append(line)
                        except ValueError:
                            pass
                elif (allomaskoz != ''):
                    with open("/home/joost/Ttar/tervtar/tervtarapp/vonallancok.txt") as fv:
                         for vline in fv:
                            if kallomas in vline and vallomas in vline:
                                kozvonal = vline[:2]+".vonal"
                                if kozvonal == '30.vonal':
                                    kozvonal = '30b.vonal'
                                koz = vline[vline.find(kallomas):vline.find(vallomas)+len(vallomas)]
                                fv.close()
                                break
                    fv.close()
                    allomasok = koz.split('-')
                    for a in allomasok:
                        if '_' in a:
                            a = charchange(a)
                        if egyseg == '' and dokumentum != '':
                            if dokumentum in line and a in line and kozvonal in line:
                                line = Path(line)
                                folderstruct.append(line)
                                break
                        elif egyseg != '' and dokumentum == '':
                            if egyseg in line and a in line and kozvonal in line:
                                line = Path(line)
                                folderstruct.append(line)
                                break 
                        elif egyseg == '' and dokumentum == '':
                            if a in line and kozvonal in line:
                                line = Path(line)
                                folderstruct.append(line)
                                break 
                else:
                    line = Path(line)
                    folderstruct.append(line)
        f.close()
    return render (request=request, template_name='folder.html', context={'elements': folderstruct})

def changepassword(request):
    if request.method == 'POST':
        form = MyPwdChForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Sikeres jelszómódosítás.")
            return redirect("/")
        else:
            messages.error(request, "Hiba történt a jelszó megváltozatása közben.")
    else:
        messages.error(request, "Hiba történt a jelszó megváltozatása közben.")
    form = MyPwdChForm(request.user)
    return render(request, 'changepw.html', {'form': form})

def addallomas(request):
    if request.method == 'POST':
        if request.user.groups.filter(name = 'Módosítók').exists():
            form = AllomasAddForm(request.POST)
            allomasok = [(a.allomasnev) for a in Allomas.objects.all()]
            vonalak = [(v.vonalszam) for v in Vonal.objects.all()]
            if form.is_valid():
                allomasnev = form.cleaned_data['allomasnev']
                vonal = form.cleaned_data['vonalszam']
                if vonal in vonalak and allomasnev not in allomasok:
                    a = Allomas(allomasnev, vonal)
                    a.save()
                    messages.success(request, "Az állomás sikeresen hozzáadva a listához.")
                    return redirect("/")
                else:
                    messages.error(request, "Az állomás már a listában van vagy a vonal nem található a listában.")
            else:
                messages.error(request, "Hiba történt az állomás hozzáadása során.")
        else:
            messages.error(request, "Állomás hozzáadása nem sikerült. Nincs hozzá jogosultságod.")
            return redirect("/")
    else:
        messages.error(request, "Hiba történt az állomás hozzáadása során.")
    form = AllomasAddForm()
    return render(request, 'addallomas.html', {'form': form}) 

def addvonal(request):
    if request.method == 'POST':
        if request.user.groups.filter(name = 'Módosítók').exists():
            form = VonalAddForm(request.POST)
            vonalak = [(v.vonalszam) for v in Vonal.objects.all()]
            if form.is_valid():
                vonal = form.cleaned_data['vonalszam']
                kezdo_allomas = form.cleaned_data['kezdo_allomas']
                vegallomas = form.cleaned_data['vegallomas']
                if vonal not in vonalak:
                    v = Vonal(vonal, kezdo_allomas, vegallomas)
                    v.save()
                    messages.success(request, "A vonal sikeresen hozzáadva a listához.")
                    return redirect("/")
                else:
                    messages.error(request, "Az vonalszám már a listában van.")
            else:
                messages.error(request, "Hiba történt a vonal hozzáadása során.")
        else:
            messages.error(request, "A vonal hozzáadása nem sikerült. Nincs hozzá jogosultságod.")
            return redirect("/")
    else:
        messages.error(request, "Hiba történt a vonal hozzáadása során.")
    form = VonalAddForm()
    return render(request, 'addvonal.html', {'form': form})