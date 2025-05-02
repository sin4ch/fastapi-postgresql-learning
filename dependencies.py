from typing import Optional

async def common_parameters(skip: int = 0, limit: Optional[int] = 100):
    return {"skip": skip, "limit": limit}
