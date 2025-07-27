from fastapi import APIRouter, HTTPException

router = APIRouter()

user_super_spark = {"remaining": 3}

@router.get("/api/super_spark/remaining")
def get_remaining_super_spark():
    return {"remaining": user_super_spark["remaining"]}

@router.post("/api/super_spark/use")
def use_super_spark():
    if user_super_spark["remaining"] > 0:
        user_super_spark["remaining"] -= 1
        return {"message": "Super Spark used.", "remaining": user_super_spark["remaining"]}
    else:
        raise HTTPException(status_code=400, detail="No Super Sparks left this week.")
