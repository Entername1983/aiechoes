from app.dependencies.settings import get_settings
from posthog import Posthog

settings = get_settings()


class DummyPosthog:
    def capture(self, *args, **kwargs):
        pass


def setup_post_hog():
    if settings.monitoring.monitoring_enabled is True:
        posthog = Posthog(
            project_api_key=settings.monitoring.post_hog_api_key,
            host=settings.monitoring.post_hog_host,
        )
        return posthog
    else:
        posthog = DummyPosthog()
        return posthog
