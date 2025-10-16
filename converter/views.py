
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Conversion
from django.conf import settings

COINGECKO_SIMPLE_PRICE = "https://api.coingecko.com/api/v3/simple/price"
COINGECKO_SUPPORTED = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"

def index(request):
    return render(request, 'converter/index.html', {})

@require_http_methods(["GET"])
def supported_currencies(request):
    """Return supported fiat/crypto vs_currencies list (cached client-side)."""
    r = requests.get(COINGECKO_SUPPORTED, timeout=10)
    if r.status_code != 200:
        return JsonResponse({'error':'failed to fetch supported currencies'}, status=500)
    return JsonResponse(r.json(), safe=False)

@require_http_methods(["POST"])
def convert(request):
    """
    POST payload: { from_currency, to_currency, amount }
    Server-side proxy to CoinGecko to avoid CORS and hide rate logic.
    """
    data = request.POST or request.json() if hasattr(request, 'json') else request.POST
    from_currency = data.get('from_currency')
    to_currency = data.get('to_currency')
    amount = data.get('amount')

    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError()
    except Exception:
        return HttpResponseBadRequest("Invalid amount")

    # For crypto->fiat or crypto->crypto: query simple/price endpoint
    params = {
        'ids': from_currency.lower(),
        'vs_currencies': to_currency.lower()
    }
    try:
        resp = requests.get(COINGECKO_SIMPLE_PRICE, params=params, timeout=10)
        resp.raise_for_status()
        j = resp.json()
    except Exception as e:
        return JsonResponse({'error':'failed to fetch rates', 'detail': str(e)}, status=500)

    try:
        rate = j[from_currency.lower()][to_currency.lower()]
    except Exception:
        return JsonResponse({'error':'pair not found in API response', 'api_response': j}, status=400)

    converted = rate * amount

    # Save history
    user = request.user if request.user.is_authenticated else None
    Conversion.objects.create(
        user=user,
        from_currency=from_currency.lower(),
        to_currency=to_currency.lower(),
        from_amount=amount,
        to_amount=converted,
        raw_rate=rate
    )

    return JsonResponse({
        'from_currency': from_currency.lower(),
        'to_currency': to_currency.lower(),
        'from_amount': amount,
        'to_amount': converted,
        'rate': rate
    })
