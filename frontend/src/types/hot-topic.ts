export interface HotTopic {
  id: number;
  title: string;
  url: string;
  source: 'zhihu' | 'weibo';
  rank: number;
  hot_value?: string;
  created_at: string;
  updated_at: string;
}

export interface HotTopicQuery {
  source?: 'zhihu' | 'weibo';
  limit?: number;
} 