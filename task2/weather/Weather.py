import requests
import csv
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}
if __name__ == "__main__":
    fileDay = "inf_day.csv"
    fileHour = "inf_hour.csv"
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=26.05942&longitude=119.198&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum,sunshine_duration&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m,is_day,shortwave_radiation"
    # 返回的是一个json文件
    data = requests.get(url=url, headers=headers)
    inf: dict
    inf = data.json()
    # 分别获取时间和天的变量
    hour_data: dict
    hour_data = inf.get("hourly")
    day_data: dict
    day_data = inf.get("daily")
    # 以下全是小时变量
    temperature_2m: list
    temperature_2m = hour_data.get("temperature_2m")
    relative_humidity_2m: list
    relative_humidity_2m = hour_data.get("relative_humidity_2m")
    apparent_temperature: list
    apparent_temperature = hour_data.get("apparent_temperature")
    precipitation: list
    precipitation = hour_data.get("precipitation")
    weather_code: list
    weather_code = hour_data.get("weather_code")
    cloud_cover_total: list
    cloud_cover_total = hour_data.get("cloud_cover")
    wind_speed_10m: list
    wind_speed_10m = hour_data.get("wind_speed_10m")
    wind_direction_10m: list
    wind_direction_10m = hour_data.get("wind_direction_10m")
    shortwave_radiation_instant: list
    shortwave_radiation_instant = hour_data.get("shortwave_radiation")
    is_day: list
    is_day = hour_data.get("is_day")
    # 以下全是每天变量
    temperature_2m_mean: list
    temperature_2m_mean = day_data.get("temperature_2m_mean")
    temperature_2m_max: list
    temperature_2m_max = day_data.get("temperature_2m_max")
    temperature_2m_min: list
    temperature_2m_min = day_data.get("temperature_2m_min")
    precipitation_sum: list
    precipitation_sum = day_data.get("precipitation_sum")
    sunshine_duration: list
    sunshine_duration = day_data.get("sunshine_duration")
    with open(fileHour, "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "cloud_cover_total",
                "wind_speed_10m",
                "wind_direction_10m",
                "shortwave_radiation_instant",
                "is_day",
            ]
        )
        for i in range(0, 8783):
            writer.writerow(
                [
                    temperature_2m[i],
                    relative_humidity_2m[i],
                    apparent_temperature[i],
                    precipitation[i],
                    weather_code[i],
                    cloud_cover_total[i],
                    wind_speed_10m[i],
                    wind_direction_10m[i],
                    shortwave_radiation_instant[i],
                    is_day[i],
                ]
            )
    with open(fileDay, "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "temperature_2m_mean",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "sunshine_duration",
            ]
        )
        for i in range(0, 365):
            writer.writerow(
                [
                    temperature_2m_mean[i],
                    temperature_2m_max[i],
                    temperature_2m_min[i],
                    precipitation_sum[i],
                    sunshine_duration[i],
                ]
            )

print("数据已成功写入CSV文件！")
