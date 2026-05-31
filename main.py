from dotenv import load_dotenv
from custom_io.IOController import IOController
from stages import *

stages = [
    # DistrictStage,
    # TrashStage,
    # ClimateStage,
    FinalStageX
]

if __name__ == "__main__":
    print("Extrator de Dados V. 3.0\n")
    load_dotenv()
    io_controller = IOController()
    data_heap, entities_to_reuse = io_controller.load_data(stages)

    print("Processando estágios...")
    for i, stage_class in enumerate(stages):
        print(f"\t[{i+1}/{len(stages)}] {stage_class.__name__}")
        stage = stage_class(data_heap)
        generated_entity, df_content = stage.model_data()
        print("\tFeito!")

        print("\t\tGravando...")
        io_controller.persist_dataframe(generated_entity, df_content)
        print("\tFeito!")

        if stage.generated_entity in entities_to_reuse:
            data_heap[stage.generated_entity.key] = df_content
