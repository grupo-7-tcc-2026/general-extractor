import os
from datetime import datetime

import pandas as pd
from modules.custom_io.Boto3Cursor import Boto3Cursor
from modules.custom_io.BytesParser import BytesParser
from modules.entities import Entity
from modules.stages.IStage import IStage


class IOController:

    s3_cursor: Boto3Cursor

    def __init__(self):
        self.s3_cursor = Boto3Cursor()

    def load_data(self, stages: list[IStage]) -> tuple[dict[str, pd.DataFrame|dict], set[Entity]]:
        print("Iniciando leitura de entidades...")
        entities_to_load, entities_to_reuse = self._reuse_or_load(stages)

        data_heap: dict[str, pd.DataFrame|dict] = {}
        for i, entity in enumerate(entities_to_load):
            print(f"\t[{i+1}/{len(entities_to_load)}] {entity.key}...")
            entity.bucket.load_name()
            data_heap[entity.key] = self._load_entity_data(entity)

        print("Feito!\n")
        return data_heap, entities_to_reuse

    def persist_dataframe(self, entity: Entity, df: pd.DataFrame) -> None:
        bytes_content = BytesParser.parse_write_content(entity, df)
        self.s3_cursor.gravar(entity, bytes_content)

    def load_dates(self):
        start_date = os.getenv("START_DATE")
        end_date = os.getenv("END_DATE")
        if start_date is None or end_date is None:
            raise EnvironmentError("Defina os parâmetros temporais no .env")

        DATE_FORMAT = "%d/%m/%Y"
        try:
            start_date = datetime.strptime(start_date, DATE_FORMAT)
            end_date = datetime.strptime(end_date, DATE_FORMAT)
        except ValueError:
            raise ValueError(
                f"O formato de data de \'{start_date}\' ou \'{end_date}\' não está de acordo com o padrão definido "
                f"(\'{DATE_FORMAT}\')"
            )
        return start_date, end_date

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
        parsed_content = BytesParser.parse_read_content(entity, bytes_content)
        return parsed_content
