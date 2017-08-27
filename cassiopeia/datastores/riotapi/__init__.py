from typing import Iterable, Set, Dict

from datapipelines import CompositeDataSource
from .common import RiotAPIService, RiotAPIRateLimiter


def _default_services(api_key: str, limiting_share: float = 1.0, handler_configs: Dict = None) -> Set[RiotAPIService]:
    from ..common import HTTPClient
    from ..image import ImageDataSource
    from .staticdata import StaticDataAPI
    from .champion import ChampionAPI
    from .summoner import SummonerAPI
    from .championmastery import ChampionMasteryAPI
    from .runepage import RunePageAPI
    from .masterypage import MasteryPageAPI
    from .match import MatchAPI
    from .spectator import SpectatorAPI
    from .status import StatusAPI
    from .leagues import LeaguesAPI

    app_rate_limiter = RiotAPIRateLimiter(limiting_share=limiting_share)

    client = HTTPClient()
    services = {
        ImageDataSource(client),
        ChampionAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        StaticDataAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        SummonerAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        ChampionMasteryAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        RunePageAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        MasteryPageAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        MatchAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        SpectatorAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        StatusAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client),
        LeaguesAPI(api_key, app_rate_limiter=app_rate_limiter, handler_configs=handler_configs, http_client=client)
    }

    return services


class RiotAPI(CompositeDataSource):
    def __init__(self, api_key: str, services: Iterable[RiotAPIService] = None, limiting_share: float = 1.0, handler_configs: Dict = None) -> None:
        if services is None:
            services = _default_services(api_key=api_key, limiting_share=limiting_share, handler_configs=handler_configs)

        super().__init__(services)

    def set_api_key(self, key: str):
        for sources in self._sources.values():
            for source in sources:
                if isinstance(source, RiotAPIService):
                    source._headers["X-Riot-Token"] = key
