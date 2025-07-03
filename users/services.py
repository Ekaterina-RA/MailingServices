from django.core.cache import cache


def get_user_stats(user_id):
    cache_key = f"user_stats_{user_id}"
    stats = cache.get(cache_key)

    if stats is None:
        stats = calculate_stats(user_id)  # функция расчета статистики
        cache.set(cache_key, stats, timeout=60 * 60)  # Кешируем на 1 час

    return stats
