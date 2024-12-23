import logging
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

class Friend:
    """
    代表一个朋友的博客信息。
    """
    def __init__(self, name, blog_url, avatar, feed_url=None, feed_type=None):
        self.name = name
        self.blog_url = blog_url
        self.avatar = avatar
        self.feed_url = feed_url
        self.feed_type = feed_type
        self.articles = []

    def add_articles(self, articles):
        """
        添加文章到朋友的博客数据中
        """
        self.articles.extend(articles)

    def clear_articles(self):
        """
        清空该朋友的文章数据
        """
        self.articles = []

class FriendLinkManager:
    """
    负责管理与爬取友链数据。
    """

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
        }
        self.timeout = (10, 15)  # 连接超时和读取超时

    def fetch_friend_data(self):
        """
        获取所有朋友的博客数据，尝试抓取每个博客的 RSS 或 Atom 信息
        """
        logging.info("开始尝试获取友链列表...")
        spider_settings = self.config.get_spider_settings()
        friends_data = self._load_friends_data(spider_settings['json_url'])
        friends = []

        logging.info(f"共有 {len(friends_data['friends'])} 位朋友，开始抓取数据...")
        for friend in friends_data['friends']:
            try:
                result = self._process_friend(friend)
                friends.append(result)
            except Exception as e:
                logging.error(f"处理友链 {friend['name']} 时出现错误：{e}", exc_info=True)
                
        logging.info(f"友链数据抓取完成，共有 {len(friends)} 位朋友")

        return friends

    def merge_data(self, result, lost_friends):
        """
        合并数据，去重处理
        """
        logging.info("开始合并数据...")
        if 'article_data' in lost_friends:
            logging.info(f"原数据文章 {len(result['article_data'])} 篇，丢失数据文章 {len(lost_friends['article_data'])} 篇")
            result['article_data'].extend(lost_friends['article_data'])
            result['article_data'] = list({v['link']: v for v in result['article_data']}.values())
        logging.info("数据合并完成")
        return result, lost_friends

    def save_data_to_files(self, result, lost_friends):
        """
        将数据保存到文件
        """
        self._save_to_json(result, 'friend_data.json')
        self._save_to_json(lost_friends, 'lost_friends.json')
        logging.info("数据保存完成")

    def _load_friends_data(self, json_url):
        """
        从 URL 加载朋友数据
        """
        try:
            response = self.session.get(json_url, headers=self.headers, timeout=self.timeout)
            return response.json()
        except Exception as e:
            logging.error(f"无法获取链接：{json_url} ：{e}", exc_info=True)
            return {'friends': []}

    def _process_friend(self, friend_data):
        """
        处理单个朋友的博客信息
        """
        name = friend_data[0]
        blog_url = friend_data[1]
        avatar = friend_data[2]

        # 获取对应的 feed 信息
        feed_type, feed_url = self._check_feed(blog_url)
        print(f"{name} 的博客 {blog_url} 的 feed 类型为 {feed_type}")
        friend = Friend(name, blog_url, avatar, feed_url, feed_type)

        if feed_type != 'none':
            feed_info = self._parse_feed(feed_url)
            articles = [
                {
                    'title': article['title'],
                    'created': article['published'],
                    'link': article['link'],
                    'author': name,
                    'avatar': avatar
                }
                for article in feed_info['articles']
            ]
            friend.add_articles(articles)
            logging.info(f"{name} 发布了 {len(articles)} 篇新文章")
        else:
            logging.warning(f"{name} 的博客 {blog_url} 无法访问")
        
        return friend

    def _check_feed(self, blog_url):
        """
        检查并返回一个博客的 RSS 或 Atom 链接
        """
        possible_feeds = [
            ('atom', '/atom.xml'),
            ('rss2', '/rss2.xml'),
            ('feed', '/feed')
        ]

        for feed_type, path in possible_feeds:
            feed_url = blog_url.rstrip('/') + path
            try:
                response = self.session.get(feed_url, headers=self.headers, timeout=self.timeout)
                if response.status_code == 200:
                    return feed_type, feed_url
            except requests.RequestException:
                continue

        return 'none', blog_url

    def _parse_feed(self, url):
        """
        解析 RSS 或 Atom feed 返回文章信息
        """
        # 这里只是返回一个示例结构，具体实现根据你的代码进行解析
        return {
            'website_name': 'Example Site',
            'author': 'Example Author',
            'link': url,
            'articles': [
                {'title': 'Example Article', 'published': '2024-12-23 12:00', 'link': url}
            ]
        }

    def _save_to_json(self, data, filename):
        """
        保存数据到 JSON 文件
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"{filename} 保存成功")

