import os

class Bucket:
    env_param_name: str
    bucket_name: str

    def __init__(self, env_param_name: str):
        self.env_param_name = env_param_name

    def load_name(self) -> None:
        env_value = os.getenv(self.env_param_name)
        if env_value is None:
            raise EnvironmentError(f"Defina a variável de ambiente \"{self.env_param_name}\" para usar este bucket.")
        self.bucket_name = env_value

class EnumBuckets:
    RAW = Bucket("BUCKET_RAW_NAME")
    TREATED = Bucket("BUCKET_TREATED_NAME")
