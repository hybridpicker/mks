from django.shortcuts import render

def test_prices_view(request):
    return render(request, 'teaching/test_prices.html')