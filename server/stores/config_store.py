# Config Store
# Save configuration in local kv store or database

import os
from typing import Optional, Dict
from llama_index.core.storage.kvstore import SimpleKVStore
from config import STORAGE_DIR, CONFIG_STORE_FILE

DATA_TYPE = Dict[str, Dict[str, dict]]

PERSISIT_PATH = "./" + STORAGE_DIR + "/" + CONFIG_STORE_FILE

class LocalKVStore(SimpleKVStore):
    #Simple Key-Value store with local persistent.

    def __init__(
        self,
        data: Optional[DATA_TYPE] = None,
    ) -> None:
        """Init a SimpleKVStore."""
        super().__init__(data)

    def put(self, key: str, val: dict) -> None:
        """Put a key-value pair into the store."""
        super().put(key=key, val=val)
        super().persist(persist_path=self.persist_path)

    def delete(self, key: str) -> bool:
        """Delete a value from the store."""
        try:
            super().delete(key)
            super().persist(persist_path=self.persist_path)
            return True
        except KeyError:
            return False
        
    @classmethod
    def from_persist_path(
        cls, persist_path: str = PERSISIT_PATH
    ) -> "LocalKVStore":
        """Load a SimpleKVStore from a persist path and filesystem."""
        cls.persist_path = persist_path
        if (os.path.exists(persist_path)):
            return super().from_persist_path(persist_path=persist_path)
        else:
            return cls({})

CONFIG_STORE = LocalKVStore.from_persist_path()