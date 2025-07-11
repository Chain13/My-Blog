from django.http import JsonResponse

def word_lists_api(request):
    return JsonResponse({
        "blacklist": ["foo", "bar", "baz"],
        "whitelist": [
            "temple", "detective", "passion", "routine", "gear", "doctor",
            "policy", "study", "truth", "animal"
        ]
    })