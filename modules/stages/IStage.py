from abc import ABC, abstractmethod
import pandas as pd
from entities import Entity


class IStage(ABC):

    data_heap: dict[str, pd.DataFrame|dict]
    required_entities: list[Entity]
    generated_entity: Entity

    def __init__(self, data_heap: dict[str, pd.DataFrame|dict]):
        if self.required_entities is None or self.generated_entity is None:
            raise AttributeError(
                "Defina as entidades necessárias e a entidade gerada para instanciar"
                " uma classe-filha de IStage"
            )
        self.data_heap = data_heap

    @abstractmethod
    def _model_data(self) -> pd.DataFrame:
        pass

    def model_data(self) -> pd.DataFrame:
        data = self._model_data()
        generated_entity = self.generated_entity
        generated_entity.bucket.load_name()
        return generated_entity, data
