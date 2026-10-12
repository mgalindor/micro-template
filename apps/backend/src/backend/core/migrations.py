from pathlib import Path

from alembic.command import upgrade
from alembic.config import Config

# repo_root/src/backend/core/migrations.py -> repo_root (apps/backend)
_REPO_ROOT = Path(__file__).resolve().parents[3]
_ALEMBIC_INI_PATH = _REPO_ROOT / "alembic.ini"


def upgrade_schema_to_head() -> None:
    """Aplica las migraciones pendientes de Alembic hasta 'head'.

    Bloqueante: debe invocarse desde un hilo aparte (p. ej. `asyncio.to_thread`)
    cuando se llama desde código async, ya que `migrations/env.py` usa `asyncio.run`.
    """
    alembic_config = Config(str(_ALEMBIC_INI_PATH))
    upgrade(alembic_config, "head")
