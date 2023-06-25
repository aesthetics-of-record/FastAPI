from fastapi import APIRouter

router = APIRouter(
	prefix='/blog',
	tags=['blog']
)

@router.post('/')
def create_blog():
	pass