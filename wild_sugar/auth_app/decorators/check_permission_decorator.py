from django.http import JsonResponse

# from restframework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import AccessToken

# def authenticate(func, permission=None):
#     def decorator(request, *args, **kwargs):
#         print(request)
#         # if not request.is_ajax():
#         #     return 'HttpResponseBadRequest()'
#         return func(request, *args, **kwargs)

#     return decorator

def authorize(args1):
    def authenticate(drf_custom_method):
        """ django-rest-framework permission decorator for custom methods """
        def decorator(self, *args, **kwargs):
            
            # token = self.request.META.get('HTTP_AUTHORIZATION', None)
            # if not token:
            #     return JsonResponse({'message':'Unauthorized access, invalid details.', 'status':False, 'status_code':401}, status=401)
            
            
            # user_details = AccessToken(token.split(" ")[1])
            # print(user_details['user_id'])
            
            if True:
                print(args1)
                return drf_custom_method(self, *args, **kwargs)
            return JsonResponse({'message':'Unauthorized access, invalid details.', 'status':False, 'status_code':400}, status=200)
        return decorator
    return authenticate


# def the_decorator(arg1, arg2):

#     def _method_wrapper(view_method):

#         def _arguments_wrapper(request, *args, **kwargs) :
#             """
#             Wrapper with arguments to invoke the method
#             """

#             #do something with arg1 and arg2

#             return view_method(request, *args, **kwargs)

#         return _arguments_wrapper

#     return _method_wrapper

