import axios from 'axios';
import type { HotTopic, HotTopicQuery } from '@/types/hot-topic';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 5000
});

export const getHotTopics = async (params?: HotTopicQuery): Promise<HotTopic[]> => {
  const { data } = await api.get('/hot-topics', { params });
  return data;
};

export const getHotTopicsBySource = async (source: 'zhihu' | 'weibo', limit?: number): Promise<HotTopic[]> => {
  const { data } = await api.get(`/hot-topics/${source}`, { params: { limit } });
  return data;
}; 