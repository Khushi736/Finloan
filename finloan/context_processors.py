from .models import LoanCategory

def loan_categories(request):
    return {
        'categories': LoanCategory.objects.filter(
            is_active=True
        )
    }