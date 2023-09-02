# Generated by Django 3.0.3 on 2022-09-03 22:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='EC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ec_name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_id', models.CharField(db_index=True, max_length=256)),
                ('entity', models.CharField(max_length=256)),
                ('start', models.IntegerField(blank=True)),
                ('stop', models.IntegerField(blank=True)),
                ('sense', models.CharField(max_length=1)),
                ('start_codon', models.CharField(default='M', max_length=1)),
                ('access', models.IntegerField(default=0)),
                ('ec', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='social.EC')),
            ],
        ),
        migrations.CreateModel(
            name='Sequencing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequencing_factory', models.CharField(max_length=256)),
                ('factory_location', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=256)),
                ('product', models.CharField(max_length=256)),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.Gene')),
            ],
        ),
        migrations.CreateModel(
            name='GeneAttributeLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='social.Attribute')),
                ('gene', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='social.Gene')),
            ],
        ),
        migrations.AddField(
            model_name='gene',
            name='sequencing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='social.Sequencing'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='gene',
            field=models.ManyToManyField(through='social.GeneAttributeLink', to='social.Gene'),
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(blank=True, max_length=256, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]