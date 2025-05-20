from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.core.config import settings

router = APIRouter()

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    windSpeed: float

@router.get("/weather/location")
async def get_location(city: str):
    """
    获取城市ID
    """
    try:
        async with httpx.AsyncClient() as client:
            # 使用城市搜索API
            response = await client.get(
                "https://pd7p3ymyfp.re.qweatherapi.com/geo/v2/city/lookup",
                params={
                    "location": city,
                    "key": settings.QWEATHER_API_KEY,
                    "range": "cn",  # 限定在中国范围内搜索
                    "number": 1     # 只返回第一个匹配结果
                }
            )
            response.raise_for_status()
            data = response.json()

            if data["code"] != "200":
                raise HTTPException(status_code=400, detail=f"和风天气API错误: {data['code']}")

            if not data.get("location"):
                raise HTTPException(status_code=404, detail=f"未找到城市: {city}")

            location = data["location"][0]
            return {
                "locationId": location["id"],
                "city": location["name"]
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"请求和风天气API失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取城市信息失败: {str(e)}")

@router.get("/weather/current")
async def get_current_weather(location: str, city_name: str):
    """
    获取指定城市的当前天气
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://pd7p3ymyfp.re.qweatherapi.com/v7/weather/now",
                params={
                    "location": location,
                    "key": settings.QWEATHER_API_KEY,
                    "lang": "zh"  # 使用中文
                }
            )
            response.raise_for_status()
            data = response.json()

            if data["code"] != "200":
                raise HTTPException(status_code=400, detail=f"和风天气API错误: {data['code']}")

            weather_data = data["now"]
            return {
                "city": city_name,  # 使用传入的城市名称
                "temperature": float(weather_data["temp"]),
                "description": weather_data["text"],
                "humidity": int(weather_data["humidity"]),
                "windSpeed": float(weather_data["windSpeed"])
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"请求和风天气API失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取天气信息失败: {str(e)}") 