import pandas as pd
from custom_io.Boto3Cursor import Boto3Cursor
from custom_io.BytesParser import BytesParser
from entities import Entity
from stages.IStage import IStage


class IOController:

    s3_cursor: Boto3Cursor

    def __init__(self):
        self.s3_cursor = Boto3Cursor()

    def load_data(self, stages: list[IStage]) -> tuple[dict[str, pd.DataFrame|dict], set[Entity]]:
        entities_to_load, entities_to_reuse = self._reuse_or_load(stages)

        data_heap: dict[str, pd.DataFrame|dict] = {}
        for entity in entities_to_load:
            entity.bucket.load_name()
            data_heap[entity.key] = self._load_entity_data(entity)

        return data_heap, entities_to_reuse

    def persist_dataframe(self, entity: Entity, df: pd.DataFrame) -> None:
        self.s3_cursor.gravar(entity, df)

    def _reuse_or_load(self, stages: list[IStage]) -> tuple[set[Entity], set[Entity]]:
        entities_to_reuse: set[Entity] = set()
        required_entities: set[Entity] = set()

        for stage in stages:
            entities_to_reuse.add(stage.generated_entity)

            for required_entity in stage.required_entities:
                required_entities.add(required_entity)

        entities_to_load = required_entities - entities_to_reuse
        return entities_to_load, entities_to_reuse

    def _load_entity_data(self, entity: Entity) -> pd.DataFrame|dict:
        bytes_content = self.s3_cursor.ler(entity)
        parsed_content = BytesParser.parse_content(entity, bytes_content)
        return parsed_content
