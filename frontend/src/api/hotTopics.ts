import { HotTopic } from '@/types/hotTopic';

export const fetchHotTopics = async (): Promise<HotTopic[]> => {
  try {
    const response = await fetch('/api/v1/hot-topics');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching hot topics:', error);
    return [];
  }
}; 