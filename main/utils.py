from django.conf import settings
from django.db import connection


class _DataBaseLoader:
    def __init__(self):
        self.posts_on_page = 12

    def load_posts(self, _search_term: str, _offset: int):
        search_term = _search_term
        offset = (
            _offset if _offset != -2 else "(SELECT MAX(main_post.id) FROM main_post)"
        )

        with connection.cursor() as cursor:
            if search_term != "":
                if search_term.startswith("tag::") and " " not in search_term:
                    cursor.execute(
                        f"""
                        SELECT main_post.*, 
                               GROUP_CONCAT(main_tag.name) AS tag_names, 
                               GROUP_CONCAT(main_tag.color) AS tag_colors, 
                               main_profile.username 
                        FROM main_post 
                        INNER JOIN main_profile ON main_profile.id = main_post.author_id 
                        LEFT JOIN main_post_tags ON main_post_tags.post_id = main_post.id 
                        LEFT JOIN main_tag ON main_tag.id = main_post_tags.tag_id 
                        WHERE main_post.id <= {offset}
                        GROUP BY main_post.id 
                        HAVING FIND_IN_SET('#{search_term[5:]}', GROUP_CONCAT(main_tag.name)) > 0
                        ORDER BY main_post.id DESC 
                        LIMIT {self.posts_on_page};
                        """
                    )
                elif search_term.startswith("category::") and " " not in search_term:
                    cursor.execute(
                        f"""
                        SELECT main_post.*, 
                               GROUP_CONCAT(main_tag.name) AS tag_names, 
                               GROUP_CONCAT(main_tag.color) AS tag_colors, 
                               main_profile.username 
                        FROM main_post 
                        INNER JOIN main_profile ON main_profile.id = main_post.author_id 
                        LEFT JOIN main_post_tags ON main_post_tags.post_id = main_post.id 
                        LEFT JOIN main_tag ON main_tag.id = main_post_tags.tag_id 
                        INNER JOIN main_category ON main_category.id = main_post.category_id 
                        WHERE main_post.id <= {offset} 
                            AND main_category.name = '{search_term[10:]}'
                        GROUP BY main_post.id 
                        ORDER BY main_post.id DESC 
                        LIMIT {self.posts_on_page};
                        """
                    )
                elif search_term.startswith("collection::") and " " not in search_term:
                    pass
                else:
                    cursor.execute(
                        f"""
                        SELECT main_post.*, 
                               GROUP_CONCAT(main_tag.name) AS tag_names, 
                               GROUP_CONCAT(main_tag.color) AS tag_colors, 
                               main_profile.username 
                        FROM main_post 
                        INNER JOIN main_profile ON main_profile.id = main_post.author_id 
                        LEFT JOIN main_post_tags ON main_post_tags.post_id = main_post.id 
                        LEFT JOIN main_tag ON main_tag.id = main_post_tags.tag_id 
                        WHERE main_post.id <= {offset}
                        AND (LOWER(main_post.title) LIKE '%{search_term}%' 
                        OR LOWER(main_post.content) LIKE '%{search_term}%'
                        or LOWER(main_profile.username) LIKE '%{search_term}%') 
                        GROUP BY main_post.id 
                        ORDER BY main_post.id DESC 
                        LIMIT {self.posts_on_page};
                        """
                    )
            else:
                cursor.execute(
                    f"""
                    SELECT main_post.*, 
                           GROUP_CONCAT(main_tag.name) AS tag_names, 
                           GROUP_CONCAT(main_tag.color) AS tag_colors, 
                           main_profile.username 
                    FROM main_post 
                    INNER JOIN main_profile ON main_profile.id = main_post.author_id 
                    LEFT JOIN main_post_tags ON main_post_tags.post_id = main_post.id 
                    LEFT JOIN main_tag ON main_tag.id = main_post_tags.tag_id 
                    WHERE main_post.id <= {offset}
                    GROUP BY main_post.id 
                    ORDER BY main_post.id DESC 
                    LIMIT {self.posts_on_page};
                    """
                )
            posts = self._dict_fetchall(cursor)

        return posts

    @staticmethod
    def posts_to_json(posts: list[dict]):
        return [
            {
                "title": post["title"],
                "content": post["content"],
                "stars": str(post["stars"]),
                "identifier": post["identifier"],
                "author": post["username"],
                "author_id": str(post["author_id"]),
                "created_at": post["created_at"].strftime(settings.DATETIME_FORMAT),
                "tags": (
                    [
                        (
                            post["tag_names"].split(",")[i],
                            post["tag_colors"].split(",")[i],
                        )
                        for i in range(len(post["tag_names"].split(",")))
                    ]
                    if post["tag_names"]
                    else []
                ),
            }
            for post in posts
        ]

    @staticmethod
    def _dict_fetchall(cursor):
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


DataBaseLoader = _DataBaseLoader()