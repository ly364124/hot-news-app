import { defineStore } from 'pinia';
import type { HotTopic } from '@/types/hot-topic';
import { getHotTopics, getHotTopicsBySource } from '@/api/hot-topic';

export const useHotTopicStore = defineStore('hotTopic', {
  state: () => ({
    topics: [] as HotTopic[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchTopics(source?: 'zhihu' | 'weibo') {
      this.loading = true;
      this.error = null;
      try {
        if (source) {
          this.topics = await getHotTopicsBySource(source);
        } else {
          this.topics = await getHotTopics();
        }
      } catch (err) {
        this.error = err instanceof Error ? err.message : '获取热搜失败';
      } finally {
        this.loading = false;
      }
    },
  },
}); 