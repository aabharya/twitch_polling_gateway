from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse


def health_check(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return JsonResponse({'status': 'error', 'db': 'unreachable'}, status=500)
    return JsonResponse({'status': 'ok'})
