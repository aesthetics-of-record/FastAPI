from fastapi import APIRouter

router = APIRouter(
	tags=["notices"]
)

@router.get("/api/notices", description="공지사항 전체 가져오기")
async def read_all_notice():
	# cursor = post.find()
	# data = loads(dumps(cursor))

	return "data"
