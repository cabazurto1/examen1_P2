from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm, EditarForm
from django.http import HttpResponse
import csv
import io
from django.shortcuts import render, get_object_or_404, redirect  
productos = []

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            productos = Producto.objects.all()
            return render(request, 'listar.html', {'productos': productos})
    else:
        form = ProductoForm()
    return render(request, 'agregar.html', {'formulario': form})

def editar_producto(request, id):
    context ={}
    obj = get_object_or_404(Producto, id = id)
    form = EditarForm(request.POST or None, instance = obj)
 

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            productos = Producto.objects.all()
            return render(request, 'listar.html', {'productos': productos})
    else:
        context["form"] = form
 
    return render(request, "editar.html", context)

def eliminar_producto(request, id):
    obj = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        obj.delete()
        productos = Producto.objects.all()
        return render(request, 'listar.html', {'productos': productos})
    return render(request, 'eliminar.html', {'producto': obj})

def exportar_productos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Precio', 'Cantidad'])

    productos = Producto.objects.all().values_list('id', 'nombre', 'precio', 'cantidad')
    for producto in productos:
        writer.writerow(producto)

    return response

def importar_productos_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'importar.html', {'error': 'El archivo no es CSV'})
        
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            _, created = Producto.objects.update_or_create(
                id=column[0],
                defaults={
                    'nombre': column[1],
                    'precio': column[2],
                    'cantidad': column[3],
                }
            )
        return redirect('listar_productos')

    return render(request, 'importar.html')