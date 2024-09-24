from django.db import models
from exams.models.exams import Exam
from accounts.models.student import Student
from django.utils import timezone


class Result(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	score = models.IntegerField()
	date_taken = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.student.name} - {self.exam.title} - {self.score}'
