from fastapi import APIRouter

router = APIRouter(
	tags=["promotions"]
)

@router.get("/api/promotions", description="홍보글 전체 가져오기")
async def read_all_promotion():
	# cursor = post.find()
	# data = loads(dumps(cursor))

	return "data"
