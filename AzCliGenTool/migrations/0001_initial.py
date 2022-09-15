# Generated by Django 4.0.7 on 2022-09-15 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AzureBaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='MySubscription', max_length=100)),
                ('subscription_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceBase',
            fields=[
                ('azurebasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AzCliGenTool.azurebasemodel')),
                ('name', models.CharField(max_length=100)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='AzCliGenTool.location')),
            ],
            bases=('AzCliGenTool.azurebasemodel',),
        ),
        migrations.CreateModel(
            name='TestCli',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_cli', models.CharField(default='123', max_length=300)),
                ('resource', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AzCliGenTool.azurebasemodel')),
            ],
        ),
        migrations.CreateModel(
            name='CreateCli',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_cli', models.CharField(default='123', max_length=300)),
                ('resource_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='AzCliGenTool.azurebasemodel')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualNetwork',
            fields=[
                ('resourcebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AzCliGenTool.resourcebase')),
                ('address_space', models.CharField(default='10.0.0.0/16', max_length=100)),
            ],
            bases=('AzCliGenTool.resourcebase',),
        ),
        migrations.CreateModel(
            name='ResourceGroup',
            fields=[
                ('azurebasemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AzCliGenTool.azurebasemodel')),
                ('name', models.CharField(default='MyResourceGroup', max_length=100, unique=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AzCliGenTool.location')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AzCliGenTool.subscription')),
            ],
            bases=('AzCliGenTool.azurebasemodel',),
        ),
        migrations.AddField(
            model_name='resourcebase',
            name='resource_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AzCliGenTool.resourcegroup'),
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('resourcebase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='AzCliGenTool.resourcebase')),
                ('subnet_address', models.CharField(default='10.0.0.0/24', max_length=100, unique=True, verbose_name='Subnet Address Space')),
                ('vnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AzCliGenTool.virtualnetwork')),
            ],
            bases=('AzCliGenTool.resourcebase',),
        ),
    ]
