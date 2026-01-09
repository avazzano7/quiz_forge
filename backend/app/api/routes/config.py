from fastapi import APIRouter

router = APIRouter(prefix="/config", tags=["config"])

@router.get("")
def get_config():
    return {
        "app_name": "Quiz App",
        "version": "0.1.0",
        "features": {
            "yaml_quiz_loading": True,
            "scoring": True
        }
    }
