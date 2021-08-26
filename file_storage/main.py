from typing import Any, Dict

from fastapi import FastAPI

from .controller import Controller

app = FastAPI()
controller = Controller()


@app.post('/v1/sum')
def register_new_user(a: int, b: int) -> Dict[Any, Any]:
    res = controller.calc_sum(a, b)
    return {'status': 'ok', 'result': res}
