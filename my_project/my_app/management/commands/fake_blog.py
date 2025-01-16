from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import random
from my_app.models import Post, Comment, Reply, Rating

class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        for _ in range(3):
            User.objects.create_user(username=faker.user_name(),
                                     email=faker.email(),
                                     password = 'qwe1asd2zxc3')
            
        users = list(User.objects.all())

        for _ in range(5):
            Post.objects.create(title=faker.sentence(nb_words=5),
                                content=faker.paragraph(nb_sentences=20),
                                author=random.choice(users))
            
        posts = list(Post.objects.all())
            
        for _ in range(20):
            Comment.objects.create(post=random.choice(posts),
                                   author=random.choice(users),
                                   content=faker.paragraph(5))
            
        comments = list(Comment.objects.all())

        for _ in range(15):
            Reply.objects.create(comment=random.choice(comments),
                                 user=random.choice(users),
                                 text=faker.paragraph(1))
            
        choises = [1, 2, 3, 4, 5]
            
        for _ in range(15):
            Rating.objects.create(post=random.choice(posts),
                                  user=random.choice(users),
                                  score=random.choice(choises))
            
        self.stdout.write(self.style.SUCCESS('Seeded data successfully'))