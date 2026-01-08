from pathlib import Path
import yaml

from app.models.quiz_models import Quiz


class QuizLoadError(Exception):
    """Raised when a quiz YAML file cannot be loaded or validated."""
    pass


def load_quiz_from_yaml(path: str | Path) -> Quiz:
    """
    Load and validate a quiz from a YAML file.

    Args:
        path: Path to YAML quiz file.

    Returns:
        Quiz: Validated Quiz object.

    Raises:
        QuizLoadError: If the file cannot be read or the content is invalid.
    """
    path = Path(path)

    if not path.exists():
        raise QuizLoadError(f"Quiz file does not exist: {path}")
    
    if path.suffix not in {".yaml", ".yml"}:
        raise QuizLoadError(f"Quiz file must be a .yaml or .yml file")
    
    try:
        with path.open("r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise QuizLoadError(f"Invalid YAML format: {e}") from e
    except OSError as e:
        raise QuizLoadError(f"Could not read file: {e}") from e
    
    if raw_data is None:
        raise QuizLoadError("Quiz file is empty")
    
    try:
        return Quiz(**raw_data)
    except Exception as e:
        raise QuizLoadError(f"Quiz validation failed: {e}") from e