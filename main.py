from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class Hint(BaseModel):
    id: Optional[int] = None
    picture: Optional[str] = None
    hint: str

class Hints(BaseModel):
    counter: int
    hints: List[Hint]

app = FastAPI()
hints_data = Hints(counter=0, hints=[])

@app.get("/", response_model=Hints)
async def get_hints():
    return hints_data

@app.post("/hint/")
async def add_hint(hint: Hint):
    hint_id = hints_data.counter + 1
    new_hint = Hint(id=hint_id, hint=hint.hint)
    hints_data.hints.append(new_hint)
    hints_data.counter += 1
    return {"message": "Hint added", "counter": hints_data.counter}

@app.get("/hint/{hint_id}", response_model=Hint)
async def get_hint_by_id(hint_id: int):
    for hint in hints_data.hints:
        if hint.id == hint_id:
            return hint
    raise HTTPException(status_code=404, detail="Hint not found")