TORTOISE_ORM = {
    "connections": {"default": "sqlite://test2.db"},
    "apps": {
        "models": {
            "models": ["modelstortoise"],  # your models path
            "default_connection": "default",
        }
    },
}
