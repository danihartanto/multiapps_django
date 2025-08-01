import csv
import os
from django.shortcuts import render
from django.http import JsonResponse
import requests

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#CSV_PATH = os.path.join(BASE_DIR, 'data', 'kode_wilayah.csv')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'kode_wilayah.csv')
def load_csv():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def index(request):
    wilayah_data = load_csv()
    provinsi_list = sorted(
        {w['kode']: w['nama'].title() for w in wilayah_data if w['level'] == '1'}.items(),
        key=lambda x: x[1]
    )
    return render(request, 'cuaca/index.html', {
        'provinsi_list': provinsi_list
    })

def get_child_wilayah(request):
    kode_induk = request.GET.get('kode')
    level_target = int(request.GET.get('level'))
    wilayah_data = load_csv()
    children = [
        {'kode': w['kode'], 'nama': w['nama'].title()}
        for w in wilayah_data
        if w['level'] == str(level_target) and w['kode'].startswith(kode_induk)
    ]
    return JsonResponse(children, safe=False)

def get_prakiraan(request):
    adm4 = request.GET.get('adm4')
    api_url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={adm4}"
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        return JsonResponse(data.get("data", []), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
