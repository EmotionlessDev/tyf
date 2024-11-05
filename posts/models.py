from django.db import models


# use URLField for url to project or any object in post
# use ForeignKey to associate a post with its author
# use ManyToManyField to associate a post with its collections, tags (NOT category)
# FileField for loading pdfs for example