from django.db import models


class Result(models.Model):
    student_id = models.CharField(max_length=50, primary_key=True)
    semester_name = models.CharField(max_length=50)
    paper_1 = models.PositiveSmallIntegerField()
    paper_2 = models.PositiveSmallIntegerField()
    paper_3 = models.PositiveSmallIntegerField()
    paper_4 = models.PositiveSmallIntegerField()
    paper_5 = models.PositiveSmallIntegerField()
    paper_6 = models.PositiveSmallIntegerField()
    paper_7 = models.PositiveSmallIntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.PositiveSmallIntegerField()
    department_id = models.CharField(max_length=50)
    department_name = models.CharField(max_length=50)