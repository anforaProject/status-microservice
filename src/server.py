import time
import random
# starlette inports 
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.schemas import SchemaGenerator
import uvicorn


# db imports 

from db import Status, UserProfile
from init_db import register_tortoise
import tortoise.exceptions

# custom import 

from errors import DoesNoExist, ValidationError, UserAlreadyExists
from utils import validate_status_creation, generate_id

app = Starlette(debug=True)

register_tortoise(
    app, db_url="sqlite://memory.sql", modules={"models": ["db"]}, generate_schemas=True
)


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)

@app.route('/v1/health', methods=["GET"])
async def homepage(request):
    return JSONResponse({'status': 'running'})

@app.route('/mock')
async def moch(request):
    await User.create(
        username='anforaUser',
        password='shouldBeAHashedPassword',
        email='random@example.com'
    )

    user = await User.get(username='anforaUser')

    prof = UserProfile(
        user_id = user.id
    )

    await prof.save()

    profile = await UserProfile.all()
    prof = await profile[0].to_json()
    print(prof)
    return JSONResponse(prof)

@app.route('/v1/status/{ident}', methods=["GET"])
async def get_status_by_id(request):
    ident = request.path_params['ident']
    try:
        status = await Status.get(ident=ident)
        return JSONResponse(await status.to_json())
    except tortoise.exceptions.DoesNotExist: 
        return DoesNoExist()

@app.route('/v1/activitypub/{ident}')
async def get_ap_by_username(request):
    ident = request.path_params['ident']
    try:
        status = await Status.get(ident=ident)
        return JSONResponse(await status.to_activitystream())
    except tortoise.exceptions.DoesNotExist: 
        return DoesNoExist()

@app.route("/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)

@app.route('/v1/status/create', methods=['POST'])
async def create_new_status(request):
    
    body = await request.json()
    
    valid = await validate_status_creation_request(body)

    if valid:
        # Check that an user with this userma doesn't exists already
        
        ident = generate_id(int(round(time.time() * 1000)) + random.randint(1, 10000))        
        await Status.create(
            caption=body['username'],
            password='shouldBeAHashedPassword',
            email='random@example.com'
        )
        
    
    return ValidationError()
