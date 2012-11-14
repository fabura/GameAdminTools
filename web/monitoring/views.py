# coding=utf-8
import datetime
import re
import time
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template.defaulttags import register
from django.utils.encoding import force_unicode
from L2Admin.models import Settings
from monitoring.models import AdenaLog

__author__ = 'bulat.fattahov'

default_limits = {"max": 10000000, "min": -10000000}

def server(request, server):
    data = {"server": server}
    data.update(csrf(request))

    try:
        date_from = datetime.datetime(*(time.strptime(request.GET["date_from"], "%Y-%m-%d")[:3]))
    except:
        date_from = datetime.date.today()
    data["date_from"] = date_from

    try:
        date_to = datetime.datetime(*(time.strptime(request.GET["date_to"], "%Y-%m-%d")[:3]))
    except:
        date_to = datetime.date.today() + datetime.timedelta(days=1)
    data["date_to"] = date_to

    if request.method == 'POST': # If the form has been submitted...
        limit_max = request.POST["limits.max"]
        limit_min = request.POST["limits.min"]
        try:
            max_setting = Settings.objects.get_or_create(name='limits.max')[0]
            max_setting.value = (int)(limit_max)
            max_setting.save()
            min_setting = Settings.objects.get_or_create(name='limits.min')[0]
            min_setting.value = (int)(limit_min)
            min_setting.save()
        except:
            data["errors"] = "Проверьте вверность введенных значений!"
            max_setting, min_setting = initSettings()
    else:
        max_setting, min_setting = initSettings()

    data["limits"] = {"max": (int)(max_setting.value), "min": (int)(min_setting.value)}

    stats = AdenaLog.objects.filter(server__name=server, date__gt=date_from, date__lt=date_to)
    if stats:
        prev = stats[0]
        for stat in stats:
            stat.diff = stat.value - prev.value
            prev = stat
        data["stats"] = stats
    return render_to_response("monitoring/server.html", data)


def initSettings():
    max_setting, created = Settings.objects.get_or_create(name='limits.max')
    if created:
        max_setting.value = default_limits["max"]
        max_setting.save()

    min_setting, created = Settings.objects.get_or_create(name='limits.min')
    if created:
        min_setting.value = default_limits["min"]
        min_setting.save()
    return max_setting, min_setting


@register.filter('intspace')
def intspace(value):
    """
    Converts an integer to a string containing spaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    See django.contrib.humanize app
    """
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new)
