import yaml

class ConfigLoader:
    """
    用于加载配置文件的类, 通过该类可以获取配置文件中的各项配置,整合所有配置项便于简化代码
    """
    def __init__(self, config_file):
        """
        初始化 ConfigLoader。
        :param config_file: 配置文件的路径。
        """
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """
        从配置文件中加载配置。
        :return: 包含所有配置项的字典。
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}

    def get_spider_settings(self):
        """
        获取爬虫设置，防止空值或缺失项。
        :return: 包含爬虫设置的字典，若缺失则返回空字典或默认值。
        """
        settings = self.config.get('spider_settings', {})
        return {
            'enable': settings.get('enable', False),
            'json_url': settings.get('json_url', ''),
            'article_count': settings.get('article_count', 0),
            'merge_result': settings.get('merge_result', {}).get('enable', False),
            'merge_json_url': settings.get('merge_result', {}).get('merge_json_url', '')
        }

    def get_email_push_settings(self):
        """
        获取邮件推送设置，防止空值或缺失项。
        :return: 包含邮件推送设置的字典，若缺失则返回空字典或默认值。
        """
        settings = self.config.get('email_push', {})
        return {
            'enable': settings.get('enable', False),
            'to_email': settings.get('to_email', ''),
            'subject': settings.get('subject', ''),
            'body_template': settings.get('body_template', '')
        }

    def get_rss_subscribe_settings(self):
        """
        获取 RSS 订阅设置，防止空值或缺失项。
        :return: 包含 RSS 订阅设置的字典，若缺失则返回空字典或默认值。
        """
        settings = self.config.get('rss_subscribe', {})
        github_username = settings.get('github_username', '').strip()
        github_repo = settings.get('github_repo', '').strip()

        # 如果 github_username 或 github_repo 不存在，则返回默认值
        if not github_username or not github_repo:
            github_username = 'default-username'
            github_repo = 'default-repo'

        return {
            'enable': settings.get('enable', False),
            'github_username': github_username,
            'github_repo': github_repo,
            'your_blog_url': settings.get('your_blog_url', ''),
            'email_template': settings.get('email_template', ''),
            'website_info': settings.get('website_info', {}).get('title', '默认标题')
        }

    def get_smtp_settings(self):
        """
        获取 SMTP 设置，防止空值或缺失项。
        :return: 包含 SMTP 设置的字典，若缺失则返回空字典或默认值。
        """
        settings = self.config.get('smtp', {})
        return {
            'email': settings.get('email', ''),
            'server': settings.get('server', ''),
            'port': settings.get('port', 0),
            'use_tls': settings.get('use_tls', False)
        }

    def get_specific_rss(self):
        """
        获取特定的 RSS 订阅源，防止空值或缺失项。
        :return: 包含特定 RSS 订阅源的列表，若缺失则返回空列表。
        """
        return self.config.get('specific_RSS', [])
