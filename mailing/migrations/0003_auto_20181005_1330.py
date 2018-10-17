# Generated by Django 2.0.6 on 2018-10-05 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_auto_20180622_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtask',
            name='name',
            field=models.CharField(help_text='пример: Недельная рассылка о главном', max_length=255, verbose_name='Название рассылки'),
        ),
        migrations.AlterField(
            model_name='emailtask',
            name='start_date',
            field=models.DateField(verbose_name='Дата начала рассылки'),
        ),
        migrations.AlterField(
            model_name='emailtask',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tasks', to='post_office.EmailTemplate', verbose_name='Email шаблон'),
        ),
    ]