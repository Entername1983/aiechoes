from posthog import Posthog

from app.dependencies.settings import get_settings

settings = get_settings()


class DummyPosthog:
    def capture(self, *args, **kwargs) -> None:  # type: ignore
        pass


def setup_post_hog() -> Posthog:
    if settings.monitoring.monitoring_enabled is True:
        posthog = Posthog(
            project_api_key=settings.monitoring.post_hog_api_key,
            host=settings.monitoring.post_hog_host,
        )
        return posthog
    posthog = DummyPosthog()
    return posthog
