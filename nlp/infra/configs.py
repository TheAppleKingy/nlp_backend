from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    @property
    def conn_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:5432/{self.postgres_db}"


class RabbitMQConfig(BaseSettings):
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_host: str
    rabbitmq_queue: str

    @property
    def conn_url(self):
        return f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}@{self.rabbitmq_host}:5672"


class AppConfig(BaseSettings):
    token_expire_time: int
    secret: str
