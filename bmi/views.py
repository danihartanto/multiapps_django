from django.shortcuts import render
from .models import Bmi
from math import pi
from bokeh.plotting import curdoc, figure, show
from bokeh.embed import components
from bokeh.models import HoverTool, ColumnDataSource
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {}
    print("Script available:", "script" in context)
    print("Div available:", "div" in context)

    if request.method == "POST":
        weight_metric = request.POST.get("weight-metric")
        weight_imperial = request.POST.get("weight-imperial")

        if weight_metric:
            weight = float(weight_metric)
            height = float(request.POST.get("height-metric"))
        elif weight_imperial:
            weight = float(weight_imperial) / 2.205
            height = (float(request.POST.get("feet")) * 30.48 + float(request.POST.get("inches")) * 2.54) / 100

        bmi = (weight / (height ** 2))
        save = request.POST.get("save")
        if save == "on":
            Bmi.objects.create(user=request.user, weight=weight, height=height, bmi=round(bmi))

        if bmi < 16:
            state = "Severe Thinness"
        elif 16 <= bmi < 17:
            state = "Moderate Thinness"
        elif 17 <= bmi < 18.5:
            state = "Mild Thinness"
        elif 18.5 <= bmi < 25:
            state = "Normal"
        elif 25 <= bmi < 30:
            state = "Overweight"
        elif 30 <= bmi < 35:
            state = "Obese Class I"
        elif 35 <= bmi < 40:
            state = "Obese Class II"
        else:
            state = "Obese Class III"

        context["bmi"] = round(bmi, 2)
        context["state"] = state

    if request.user.is_authenticated:
        dates = []
        bmis = []
        num = 1
        dates_queryset = Bmi.objects.filter(user=request.user).order_by("date")
        for qr in dates_queryset:
            dates.append(str(qr.date) + f" ({num})")
            bmis.append(float(qr.bmi))
            num += 1

        source = ColumnDataSource(data=dict(
            x=dates,
            y=bmis
        ))

        curdoc().theme = 'caliber'
        plot = figure(x_range=dates, height=400, sizing_mode="stretch_width", title="BMI Statistics",
              toolbar_location="right", tools="pan,wheel_zoom,box_zoom,reset,hover,tap,crosshair")


        plot.title.text_font_size = "12pt"
        plot.xaxis.major_label_text_font_size = "10pt"
        plot.xaxis.major_label_orientation = pi / 4

        # Step plot with label for legend
        plot.step(x='x', y='y', source=source, line_width=2, legend_label="BMI Over Time", mode="after")

        # Hover tooltip config
        # hover = plot.select_one(HoverTool)
        # hover.tooltips = [("Date", "@x"), ("BMI", "@y")]

        plot.legend.label_text_font_size = "8pt"

        script, div = components(plot)
        context["script"] = script
        context["div"] = div

    return render(request, "bmi/index.html", context)
