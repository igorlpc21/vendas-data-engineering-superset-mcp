import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

PRODUTOS = [
    ('Sofá 3 Lugares', 'Móveis', 2450.00),
    ('Mesa de Jantar', 'Móveis', 1800.00),
    ('Cadeira Estofada', 'Móveis', 420.00),
    ('Guarda-Roupa', 'Móveis', 2100.00),
    ('Luminária de Mesa', 'Iluminação', 185.00),
    ('Pendente LED', 'Iluminação', 390.00),
    ('Tapete Decorativo', 'Decoração', 320.00),
    ('Espelho Redondo', 'Decoração', 260.00),
    ('Cortina Blackout', 'Têxteis', 230.00),
    ('Jogo de Almofadas', 'Têxteis', 120.00),
]
CLIENTES = ['Ana Silva', 'Bruno Costa', 'Carla Souza', 'Daniel Lima', 'Eduarda Rocha',
            'Felipe Santos', 'Gabriela Alves', 'Henrique Melo', 'Isabela Martins', 'João Oliveira',
            'Larissa Ribeiro', 'Marcos Pereira', 'Natália Gomes', 'Paulo Ferreira', 'Renata Araújo']
REGIOES = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
PAGAMENTOS = ['PIX', 'Cartão de Crédito', 'Cartão de Débito', 'Dinheiro', 'Boleto']

DESTINO = Path(__file__).resolve().parent / 'dados' / 'vendas.csv'
DESTINO.parent.mkdir(parents=True, exist_ok=True)
INICIO = date(2025, 1, 1)
FIM = date(2026, 9, 30)
DIAS = (FIM - INICIO).days

with DESTINO.open('w', newline='', encoding='utf-8-sig') as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(['id_venda', 'data_venda', 'cliente', 'produto', 'categoria', 'regiao',
                       'quantidade', 'valor_unitario', 'desconto_percentual', 'valor_total', 'forma_pagamento'])
    for i in range(1, 1001):
        produto, categoria, preco = random.choice(PRODUTOS)
        quantidade = random.randint(1, 5)
        desconto = random.choice([0, 0, 0, 5, 10, 15])
        total = round(quantidade * preco * (1 - desconto / 100), 2)
        escritor.writerow([i, (INICIO + timedelta(days=random.randint(0, DIAS))).isoformat(),
                           random.choice(CLIENTES), produto, categoria, random.choice(REGIOES),
                           quantidade, f'{preco:.2f}', desconto, f'{total:.2f}', random.choice(PAGAMENTOS)])
print(f'Arquivo criado: {DESTINO} (1.000 vendas)')
