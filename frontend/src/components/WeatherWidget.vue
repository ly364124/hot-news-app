<template>
  <div class="weather-widget">
    <div v-if="loading" class="loading">
      <el-skeleton :rows="2" animated />
    </div>
    <div v-else class="weather-content">
      <div v-if="weather" class="weather-info">
        <div class="location">{{ city }}</div>
        <div class="temperature">{{ weather.temperature }}°C</div>
        <div class="description">{{ weather.description }}</div>
        <div class="details">
          <div>湿度: {{ weather.humidity }}%</div>
          <div>风速: {{ weather.windSpeed }} km/h</div>
        </div>
      </div>
      <div v-else class="error">
        <el-alert
          title="获取天气信息失败"
          type="error"
          :closable="false"
        />
      </div>
      <div class="search-box">
        <el-input
          v-model="searchCity"
          placeholder="输入城市"
          @keyup.enter="searchWeather"
          class="city-input"
        >
          <template #append>
            <el-button @click="searchWeather">获取天气</el-button>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface WeatherData {
  temperature: number
  description: string
  humidity: number
  windSpeed: number
}

const loading = ref(true)
const weather = ref<WeatherData | null>(null)
const city = ref('深圳') // 默认城市
const searchCity = ref('') // 搜索城市

const getWeather = async (targetCity: string) => {
  loading.value = true
  try {
    const response = await axios.get(`/api/v1/weather/current?city=${encodeURIComponent(targetCity)}`)
    weather.value = response.data
    city.value = targetCity
  } catch (error) {
    console.error('获取天气失败:', error)
    weather.value = null
  } finally {
    loading.value = false
  }
}

const searchWeather = () => {
  if (searchCity.value.trim()) {
    getWeather(searchCity.value.trim())
    searchCity.value = '' // 清空搜索框
  }
}

onMounted(() => {
  getWeather(city.value) // 默认加载深圳天气
})
</script>

<style scoped>
.weather-widget {
  padding: 1rem;
  border-radius: 8px;
  background-color: #f5f5f5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  color: #666;
}

.weather-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.weather-info {
  text-align: center;
}

.location {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.temperature {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.description {
  color: #666;
}

.details {
  display: flex;
  gap: 20px;
}

.search-box {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.city-input {
  width: 200px;
}

.error {
  color: #ff4d4f;
  text-align: center;
}
</style> 