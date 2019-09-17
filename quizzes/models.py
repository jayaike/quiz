from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Quiz(models.Model):
    name = models.CharField(max_length=1000)
    questions_count = models.IntegerField(default=0)
    description = models.CharField(max_length=70)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    slug = models.SlugField()
    roll_out = models.BooleanField(default=False)

    class Meta:
        ordering = ['created',]
        verbose_name_plural ="Quizzes"

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #
    #     super(Quiz, self).save(*args, **kwargs)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=1000)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.label

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizTakers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return self.user.username

class Response(models.Model):
    quiztaker = models.ForeignKey(QuizTakers, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.question.label

@receiver(post_save, sender=Quiz)
def set_default_quiz(sender, instance, created,**kwargs):
    quiz = Quiz.objects.filter(id = instance.id)
    quiz.update(questions_count=instance.question_set.filter(quiz=instance.pk).count())

@receiver(post_save, sender=Question)
def set_default(sender, instance, created,**kwargs):
    quiz = Quiz.objects.filter(id = instance.quiz.id)
    quiz.update(questions_count=instance.quiz.question_set.filter(quiz=instance.quiz.pk).count())

@receiver(pre_save, sender=Quiz)
def slugify_title(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)
