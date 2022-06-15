from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.conf import settings

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def get_recipes():
    if "recipes" in cache:
        recipes = cache.get("recipes")
        print(f"already in cache with ttl => {cache.ttl('recipes')}")
    else:
        print("caching")
        recipes = Recipe.objects.all()  # type: ignore
        cache.set("recipes", recipes, timeout=CACHE_TTL)
    return recipes
