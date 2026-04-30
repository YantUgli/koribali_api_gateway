from app.core.config import settings

def get_internal_service_headers() -> dict:
    """
    Generate security headers for internal service-to-service communication.
    """
    return {
        "X-Internal-Key": settings.calc_service_key
    }