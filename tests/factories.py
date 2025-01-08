from polyfactory.factories.pydantic_factory import ModelFactory
from aio_space_traders import model


class ServerStatusResponseFactory(ModelFactory[model.ServerStatsResponse]): ...
