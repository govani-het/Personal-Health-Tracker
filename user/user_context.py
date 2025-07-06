from .models import UserData,ProfileSetUp


def user_context_data(request):
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserData.objects.get(user_id=user_id)
            profile = ProfileSetUp.objects.get(user_id=user_id)
            return {'user': user, 'profile': profile}
        except UserData.DoesNotExist:
            return {'user': None}
    return {'user': None}

