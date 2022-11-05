# Generated by Django 4.1.2 on 2022-11-05 01:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_produto_descricao'),
        ('venda', '0002_percentualcomissao'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdutoVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('percentual_comissao', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(0.1)])),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produto.produto')),
                ('venda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='venda.venda')),
            ],
        ),
        migrations.DeleteModel(
            name='VendaProduto',
        ),
    ]
