from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from oracle_config import run_queries, get_connection
from recommender import generate_recommendations
from summarizer import summarize_reviews_for_product
import traceback

app = FastAPI()

@app.get("/")
def home():
    return {"message": "✅ 서버 정상 동작 중"}

@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    try:
        user_df, funding_df, tag_df, image_df = run_queries(user_id)
        result = generate_recommendations(user_df, funding_df, tag_df, image_df)
        return JSONResponse(content=result, media_type="application/json")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary/{product_id}")
def summarize(product_id: int):
    try:
        summary = summarize_reviews_for_product(product_id)
        return {"productId": product_id, "summary": summary}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail="No review content found.")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

