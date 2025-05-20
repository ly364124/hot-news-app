from fastapi import APIRouter, HTTPException
import httpx
from app.core.config import settings

router = APIRouter()

@router.get("/current")
async def get_current_weather(city: str):
    """
    获取指定城市的当前天气
    """
    try:
        async with httpx.AsyncClient() as client:
            # 使用和风天气API获取天气信息
            response = await client.get(
                f"https://devapi.qweather.com/v7/weather/now",
                params={
                    "location": city,
                    "key": settings.QWEATHER_API_KEY
                }
            )
            response.raise_for_status()
            data = response.json()

            if data["code"] != "200":
                raise HTTPException(status_code=400, detail=f"和风天气API错误: {data['code']}")

            weather_data = data["now"]
            return {
                "temperature": float(weather_data["temp"]),
                "description": weather_data["text"],
                "humidity": int(weather_data["humidity"]),
                "windSpeed": float(weather_data["windSpeed"])
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"请求和风天气API失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取天气信息失败: {str(e)}") 