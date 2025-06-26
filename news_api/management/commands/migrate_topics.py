# news_api/management/commands/migrate_topics.py

from django.core.management.base import BaseCommand
from news_api.models import NewsArticle, Topic, NewsArticleTopic

class Command(BaseCommand):
    help = "Migrate topics from NewsArticle JSONField to normalized Topic and NewsArticleTopic tables"

    def handle(self, *args, **options):
        articles = NewsArticle.objects.exclude(topics=None)

        total = articles.count()
        migrated = 0

        for article in articles:
            topics_data = article.topics

            # Safeguard: skip if topics is not a list
            if not isinstance(topics_data, list):
                self.stdout.write(self.style.WARNING(f"Skipped article {article.pk}: topics is not a list"))
                continue

            for topic_entry in topics_data:
                topic_name = topic_entry.get("topic")
                relevance_score = float(topic_entry.get("relevance_score", 0))

                if not topic_name:
                    continue

                topic_obj, _ = Topic.objects.get_or_create(name=topic_name)
                NewsArticleTopic.objects.get_or_create(
                    article=article,
                    topic=topic_obj,
                    defaults={"relevance_score": relevance_score}
                )

            migrated += 1
            self.stdout.write(f"Migrated article {article.pk} ({migrated}/{total})")

        self.stdout.write(self.style.SUCCESS(f"✅ Migrated {migrated}/{total} articles successfully."))
