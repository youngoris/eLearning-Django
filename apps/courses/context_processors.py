from .models import Category

# Define a context processor to make the list of Category instances available globally to all templates
def categories_processor(request):
    categories = Category.objects.all()  
    return {'categories': categories}  
