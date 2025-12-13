from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


# def group_required(group_name):
#     def decorator(view_func):
#         def _wrapped_view(request, *args, **kwargs):
#             if request.user.groups.filter(name=group_name).exists():
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponseForbidden(
#                     "You do not have permission to view this page."
#                 )

#         return _wrapped_view

#     return decorator


def group_required(group_name, redirect_url="index"):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if (
                request.user.is_authenticated
                and request.user.groups.filter(name=group_name).exists()
            ):
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(
                    request,
                    f"Ezt az oldalt csak a(z) '{group_name}' csoport tagjai érhetik el.",
                    extra_tags="login",
                )
                return redirect(redirect_url)

        return _wrapped_view

    return decorator


def group_required_django(group_name):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name=group_name).exists(),
        login_url="index"
    )


def anonymous_required(redirect_url):
    def _wrapped(view_func, *args, **kwargs):
        def check_anonymous(request, *args, **kwargs):
            if request.user.is_authenticated:
                # return redirect(redirect_url)
                return HttpResponseForbidden(
                    "This is only for non authenticated users..."
                )
            else:
                return view_func(request, *args, **kwargs)

        return check_anonymous

    return _wrapped
