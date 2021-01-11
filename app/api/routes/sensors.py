from fastapi import APIRouter, Depends

router = APIRouter()

#
#
# @router.post(path="")
# async def add_sensor(sensor: AddSensorInput):
#     sensor_as_dict = dict(sensor)
#     _id = db.insert(**sensor_as_dict)
#     raw_sensor = db.get_one(_id=_id)
#     return Sensor(**raw_sensor)
#
#
# @router.get(path="", response_model=ListOfSensors)
# async def get_plants_list(pagination_params: PaginationParams = Depends(PaginationParams)):
#     results = pagination_params.paginate(db.all(apply=False), ListOfSensors)
#     return results
