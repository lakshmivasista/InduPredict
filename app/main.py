from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.predictor import predict_machine

app = FastAPI(
    title="InduPredict API",
    description="AI-Based Industrial Predictive Maintenance API",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


class MachineInput(BaseModel):
    machine_type: str
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float


@app.get("/")
def root():
    return FileResponse(
        "app/static/index.html"
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(input_data: MachineInput):

    result = predict_machine(
        machine_type=input_data.machine_type,
        air_temperature=input_data.air_temperature,
        process_temperature=input_data.process_temperature,
        rotational_speed=input_data.rotational_speed,
        torque=input_data.torque,
        tool_wear=input_data.tool_wear
    )

    return result