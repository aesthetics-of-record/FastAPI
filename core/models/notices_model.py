from pydantic import BaseModel


class Notice(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	classification: int