from django.db import models

# Create your models here.

class index_info(models.Model):
    id = models.AutoField(primary_key=True)
    index_code = models.CharField(null=False, max_length=16, db_index=True)
    index_name = models.CharField(null=False, max_length=32)
    index_data_table = models.CharField(max_length=32)
    index_data_fund = models.CharField(max_length=32)
    start_date = models.DateField(null=False)
    last_update_date = models.DateField(null=False)

    class Meta:  # 元信息类
        db_table = 'index_info'  # 自定义表的名字

    def delete_index_info(self, index_code):
        self.objects.filter(index_code=index_code).delete()

    def update_index_info(self, index_code, last_update_date):
        self.objects.filter(index_code=index_code).update(last_update_date=last_update_date)