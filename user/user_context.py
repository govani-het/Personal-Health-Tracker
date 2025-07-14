
from .models import UserData, ProfileSetUp

def user_context_data(request):

    context = {}
    user_id = request.session.get('user_id')

    if user_id:
        try:

            user = UserData.objects.get(user_id=user_id)
            context['user'] = user

            try:

                profile = ProfileSetUp.objects.get(user_id=user)
                context['profile'] = profile
            except ProfileSetUp.DoesNotExist:

                pass

        except UserData.DoesNotExist:

            pass

    return context