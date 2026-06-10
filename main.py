from dotenv import load_dotenv
from modules.custom_io.IOController import IOController
from modules.stages import *

stages = [
    DistrictStage,
    TrashStage,
    ClimateStage,
    DrainageStage,
    FloodingStage,
    FinalStage
]

if __name__ == "__main__":
    print("Extrator de Dados V. 4.0\n")
    load_dotenv()
    io_controller = IOController()
    data_heap, entities_to_reuse = io_controller.load_data(stages)
    start_date, end_date = io_controller.load_dates()

    print("Processando estágios...")
    for i, stage_class in enumerate(stages):
        print(f"\t[{i+1}/{len(stages)}] {stage_class.__name__}")
        stage = stage_class(data_heap, start_date, end_date)
        generated_entity, df_content = stage.model_data()
        print("\tFeito!")

        print("\t\tGravando...")
        io_controller.persist_dataframe(generated_entity, df_content)
        print("\tFeito!")

        if stage.generated_entity in entities_to_reuse:
            data_heap[stage.generated_entity.key] = df_content
