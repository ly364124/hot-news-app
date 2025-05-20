export interface HotTopic {
  id: number;
  title: string;
  url: string;
  source: string; // 例如: 'zhihu', 'weibo'
  rank: number;
  hot_value: string;
  created_at: string;
  updated_at: string;
} 