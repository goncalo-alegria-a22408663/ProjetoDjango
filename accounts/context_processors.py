def is_gestor_portfolio(request):
    if request.user.is_authenticated:
        return {
            'is_gestor': request.user.groups.filter(name='gestor-portfolio').exists()
        }
    return {'is_gestor': False}