from typing import Union
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# Base Todo Class for types and validation


class Todo(BaseModel):
    id: Union[int, None]
    status: bool
    message: str


app = FastAPI()

# Simulated storage for storing the todos (PS: This not suitable for production applications.)
todos = [
    {
        "id": 1,
        "status": False,
        "message": "To add todo."
    }
]


@app.get("/")
def get_todos():
    """
    Returns all the TODOs.
    """
    return todos


@app.post("/")
def create_todo(item: Todo):
    """
    Create a TODO.
    """

    todos.append({
        "id": len(todos),
        "status": True,
        "message": item.message
    })

    return {
        "message": "Successfully added the Todo.",
        "status": "success"
    }


@app.delete("/{index}")
def delete_todo(index: int, response: Response):
    """
    Delete a TODO by index.
    """

    try:
        todos.pop(index)

        return {
            "message": "Successfully deleted the Todo.",
            "status": "success"
        }

    except:

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "The Todo you want to delete does not exists.",
            "status": "failed"
        }
