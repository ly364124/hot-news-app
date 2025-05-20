<template>
  <div class="home-container">
    <div class="header">
      <h1 class="page-title">实时热搜榜</h1>
      <div class="meta-info">
        <p class="current-time">{{ currentTime }}</p>
        <div class="weather-display">
          <div class="weather-info" v-if="weather">
            <span class="city">{{ weather.city }}</span>
            <img :src="weatherIcon" alt="weather icon" class="weather-icon" v-if="weatherIcon"/>
            <span class="temperature">{{ weather.temperature }}°C</span>
            <span class="description">{{ weather.description }}</span>
            <span class="details">湿度: {{ weather.humidity }}%</span>
            <span class="details">风速: {{ weather.windSpeed }} km/h</span>
          </div>
          <div class="weather-loading" v-else-if="loading">
            <el-skeleton :rows="1" animated />
          </div>
          <div class="weather-error" v-else>
            <el-alert
              title="获取天气信息失败"
              type="error"
              :closable="false"
            />
          </div>
        </div>
        
        <div class="weather-search-box">
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

    <el-radio-group v-model="selectedSource" @change="handleSourceChange" class="source-tabs">
      <el-radio-button value="">全部</el-radio-button>
      <el-radio-button value="zhihu">知乎</el-radio-button>
      <el-radio-button value="weibo">微博</el-radio-button>
    </el-radio-group>

    <el-card v-for="topic in filteredHotTopics" :key="topic.id" class="hot-topic-card" @click="goToTopic(topic.url)">
      <div class="card-content">
        <span class="topic-rank">{{ topic.rank }}</span>
        <span class="topic-title">{{ topic.title }}</span>
        <span class="topic-hot-value">{{ topic.hot_value }}</span>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { ElRadioGroup, ElRadioButton, ElCard, ElSkeleton, ElAlert, ElInput, ElButton } from 'element-plus';
import axios from 'axios';
// 确保这些引入路径正确
import { fetchHotTopics } from '@/api/hotTopics'; 
import { HotTopic } from '@/types/hotTopic';

const allHotTopics = ref<HotTopic[]>([]);
const selectedSource = ref<string>('');
const currentTime = ref<string>('');
let timer: number | undefined;

const loading = ref(true);
const weather = ref<{ city: string; temperature: number; description: string; humidity: number; windSpeed: number } | null>(null);
const searchCity = ref(''); // 用于存储用户输入的城市

const weatherIcon = computed(() => {
    if (!weather.value) return null;
    const description = weather.value.description;
    console.log("Weather description:", description);
    // 这是一个示例，您需要根据实际图标文件和天气描述进行映射
    if (description.includes('多云')) return '/icons/cloudy.svg';
    if (description.includes('晴')) return '/icons/sunny.svg';
    if (description.includes('雨')) return '/icons/rainy.svg';
    if (description.includes('阴')) return '/icons/overcast.svg'; // 添加阴天图标示例
    if (description.includes('霾')) return '/icons/wumai.svg';
    // 添加更多天气描述和图标的映射
    return null; // 默认没有图标
});

const filteredHotTopics = computed(() => {
  if (!selectedSource.value) {
    return allHotTopics.value;
  } else {
    return allHotTopics.value.filter((topic: HotTopic) => topic.source === selectedSource.value);
  }
});

const loadHotTopics = async () => {
  const topics = await fetchHotTopics();
  allHotTopics.value = topics;
};

const handleSourceChange = () => {
  // 筛选逻辑已经在 computed属性中处理
};

const goToTopic = (url: string | undefined) => {
  if (url) {
    window.open(url, '_blank');
  }
};

const updateTime = () => {
  const now = new Date();
  const year = now.getFullYear();
  const month = (now.getMonth() + 1).toString().padStart(2, '0');
  const day = now.getDate().toString().padStart(2, '0');
  const hours = now.getHours().toString().padStart(2, '0');
  const minutes = now.getMinutes().toString().padStart(2, '0');
  const seconds = now.getSeconds().toString().padStart(2, '0');
  currentTime.value = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};

const getWeather = async (city: string) => {
  loading.value = true;
  try {
    // 首先获取城市ID
    const locationResponse = await axios.get(`/api/v1/weather/location?city=${encodeURIComponent(city)}`);
    const locationId = locationResponse.data.locationId;
    const cityName = locationResponse.data.city;
    
    // 使用城市ID获取天气信息，同时传递城市名称
    const weatherResponse = await axios.get(`/api/v1/weather/current?location=${locationId}&city_name=${encodeURIComponent(cityName)}`);
    weather.value = weatherResponse.data;
  } catch (error) {
    console.error('获取天气失败:', error);
    weather.value = null;
  } finally {
    loading.value = false;
  }
};

// 新增：根据用户输入获取天气
const searchWeather = () => {
  if (searchCity.value.trim()) {
    getWeather(searchCity.value.trim());
    searchCity.value = ''; // 清空输入框
  }
};

onMounted(() => {
  loadHotTopics();
  updateTime(); // Initial time call
  timer = setInterval(updateTime, 1000); // Update time every second
  getWeather('深圳'); // 默认获取深圳天气
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});

</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* 顶部对齐，防止城市输入框影响布局 */
  margin-bottom: 20px;
  flex-wrap: wrap; /* 允许换行，避免元素溢出 */
}

.page-title {
  font-size: 2em;
  color: #333;
  margin-right: 20px; /* 标题和元信息之间的间距 */
}

.meta-info {
    display: flex; /* 使时间和天气信息并排显示 */
    flex-direction: column; /* 使时间和天气信息垂直排列 */
    align-items: flex-start; /* 左对齐 */
     flex-wrap: wrap; /* 允许换行 */
}

.current-time {
  font-size: 1.2em;
  color: #555;
  margin-right: 0; /* 移除时间右边间距 */
   margin-bottom: 10px; /* 在时间和天气组件之间增加间距 */
}

.weather-display {
  margin-bottom: 15px; /* 天气显示和搜索框之间的间距 */
}

.weather-info {
  display: flex; /* 使用 Flexbox */
  align-items: center; /* 垂直居中 */
  gap: 10px; /* 元素之间的间距 */
  font-size: 1.1em;
  color: #606266;
  flex-wrap: wrap; /* 允许元素换行，防止溢出 */
}

.weather-info .city {
  font-weight: bold;
  color: #409EFF;
}

.weather-icon {
    width: 24px; /* 图标宽度 */
    height: 24px; /* 图标高度 */
    flex-shrink: 0; /* 防止图标被挤压 */
}

.weather-info .temperature {
  font-size: 1.3em;
  font-weight: bold;
  color: #303133;
}

.weather-info .description,
.weather-info .details {
  /* 可以添加一些样式，比如颜色或字体 */
  white-space: nowrap; /* 防止文字换行 */
}

.weather-loading,
.weather-error {
  margin-top: 10px;
}

.weather-search-box {
    width: 300px; /* 设置搜索框容器宽度 */
}

.city-input :deep(.el-input__wrapper) {
  border-radius: 4px 0 0 4px; /* 调整圆角 */
}

.city-input :deep(.el-input-group__append) {
  border-radius: 0 4px 4px 0; /* 调整圆角 */
}


.source-tabs {
  margin-bottom: 20px;
}

.hot-topic-card {
  margin-bottom: 15px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.hot-topic-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-content {
  display: flex;
  align-items: center;
}

.topic-rank {
  font-size: 1.2em;
  font-weight: bold;
  margin-right: 15px;
  color: #409EFF; /* Element Plus Primary color */
}

.topic-title {
  flex-grow: 1;
  font-size: 1.1em;
  margin-right: 15px;
  color: #303133;
}

.topic-hot-value {
  font-size: 0.9em;
  color: #909399; /* Element Plus Info color */
}
</style> 