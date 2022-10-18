from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import render
from django.template.loader import get_template

from .filters import ContratFilter
from .models import Contrat
from .forms import ContratForm
from django.contrib import messages

#from django.template.loader import get_template
#from xhtml2pdf import pisa

#pip install ipgeotools
#pip install xhtml2pdf

# Create your views here.
@login_required(login_url='home')
def home(request):
    homes = Contrat.objects.all().order_by('-date_creation')
    context = {'homes': homes}
    return render(request,'app/home.html', context)


#   -------------  Liste un courrier ----------------------
@login_required(login_url='home')
def list_contrat(request):
    contrats = Contrat.objects.all().order_by('-date_creation')
    total_contrats = contrats.count()
    myContratFilter = ContratFilter(request.GET, queryset=contrats)
    contrats = myContratFilter.qs
    context = {'contrats': contrats, 'total_contrats': total_contrats,'myContratFilter':myContratFilter,}
    return render(request, 'appt/listContrat.html', context)

#   -------------  Détail un courrier ----------------------
@login_required(login_url='home')
def detail_contrat(request,pk):
    contrat = Contrat.objects.get(id=pk)
    context = {'contrat': contrat,}
    return render(request, 'appt/detailContrat.html', context)

#   -------------  Ajouter ----------------------
@login_required(login_url='home')
def add_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = ContratForm()
    return render(request, 'appt/addContrat.html', {'form': form})


#   -------------  Modifier  ----------------------
@login_required(login_url='home')
def update_contrat(request,pk):
    contrat = Contrat.objects.get(id=pk)
    form = ContratForm(instance=contrat)
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES,instance=contrat)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'appt/updateContrat.html',context )

#   -------------  Supprimer un courrier ----------------------
@login_required(login_url='home')
def delete_contrat(request,pk):
    contrat = Contrat.objects.get(id=pk)
    if request.method == 'POST':
        contrat.delete()
        return redirect('home')
    context = {'contrat': contrat}
    return render(request, 'appt/deleteContrat.html', context)

#   -------------  Rechercher un courrier ----------------------
@login_required(login_url='home')
def search_contrat(request):
    query = request.GET.get('query')
    if not query:
        contrats = Contrat.objects.all()
    else:
        contrats = Contrat.objects.filter(immatriculation__icontains=query)
        if not contrats.exists():
            print("Misère de misère, nous n'avons trouvé aucun numero d'immatriculation")
        else:
            contrats = ["<li>{}<li>".format(contrats.date_creation) for constats in contrats]
            messages.success(request,"Nous avons trouvé des programmes correspondants à votre réquête les voici: " + contrats)
    titre = "Le résultat de votre recherche est: %s"%query
    context = {'contrats': contrats,
               'titre': titre}
    return render(request, 'appt/searchContrat.html', context)



# ========================================================================================
def pdf_constat(request,pk):
    contrat = get_object_or_404(Contrat, id=pk)

    template_path = 'appt/pdfContrat.html'
    context = {'contrat': contrat}

    # Create a Django response object and specify  content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf'

    # if Display:
    response['Content-Disposition'] = 'filename="report.pdf"'

    # if find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # Create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)

    # If error, then show funy view
    if pisa_status.error:
        return HttpResponse('We are some errors <pre>' + html + '<pre>')
    return response

