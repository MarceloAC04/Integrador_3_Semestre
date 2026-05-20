import matplotlib.pyplot as plt

def valores_pizza(val, valores_originais):
    total = sum(valores_originais)
    valor = int(round(val * total / 100))
    return f'{valor}\n({val:.1f}%)'


valores_gpu = [94, 5, 1.3]
nomes_gpu = ["Nvidia", "AMD", "Intel"]

plt.figure("Pizza - Mercado GPUs")

plt.pie(valores_gpu, labels=nomes_gpu, autopct=lambda pct: valores_pizza(pct, valores_gpu))

plt.title("Participação no Mercado de GPUs (Unidades Vendidas)")

plt.show()


# Gráfico de Dispersão: Preço vs Desempenho de GPUs

# Nvidia
precos_nv = [1599, 1199, 899, 799, 599, 499, 299]
desemp_nv = [30000, 24000, 18000, 15000, 10000, 8000, 5000]

# AMD
precos_amd = [999, 899, 699, 549, 499, 399, 269]
desemp_amd = [20000, 17000, 14000, 11000, 9500, 7500, 4500]

# Intel
precos_int = [329, 289, 139]
desemp_int = [8500, 7500, 4500]

plt.figure("Dispersão - GPUs: Preço vs Desempenho")

plt.scatter(precos_nv, desemp_nv, color='blue', label='Nvidia')
plt.scatter(precos_amd, desemp_amd, color='red', label='AMD')
plt.scatter(precos_int, desemp_int, color='green', label='Intel')

plt.title("GPUs: Relação entre Preço e Desempenho")
plt.xlabel("Preço de Lançamento (USD)")
plt.ylabel("Índice de Desempenho")

plt.legend()

plt.grid(True)


plt.show()


# Gráfico de Barras: Receita Estimada por Marca (GPUs) 

receita_estimada = [valores_gpu[0] * 600, valores_gpu[1] * 500, valores_gpu[2] * 250]
marcas_gpu = ["Nvidia", "AMD", "Intel"]

plt.figure("Barras - Receita Estimada GPUs")

plt.bar(marcas_gpu, receita_estimada, color=['blue', 'red', 'green'])

plt.title("Receita Estimada de GPUs por Marca")
plt.xlabel("Marca")
plt.ylabel("Receita Estimada (Preço Médio x Fatia Mercado)")

plt.show()


# Gráfico Boxplot: Distribuição de Preços de GPUs
precos_listas = [precos_nv, precos_amd, precos_int]

plt.figure("Boxplot - Preços de Lançamento GPUs")

plt.boxplot(precos_listas)

plt.xticks([1, 2, 3], ["Nvidia", "AMD", "Intel"])

plt.title("Distribuição de Preços de Lançamento de GPUs por Marca")
plt.ylabel("Preço (USD)")

plt.show()


# Gráfico Histograma: Frequência de Preços de GPUs Vendidas
precos_vendas_nv = [
    299, 399, 499, 599, 799, 899, 1199, 1599, 299, 399, 499, 299, 399, 499,
    599, 299, 399, 299, 399, 499, 299, 399, 499, 599, 299, 399, 299, 399, 299, 399
]

plt.figure("Histograma - Vendas GPUs Nvidia por Preço")

plt.hist(precos_vendas_nv, bins=8, color='blue', edgecolor='black')

plt.title("Frequência de Preços de GPUs Nvidia Vendidas")
plt.xlabel("Faixa de Preço (USD)")
plt.ylabel("Quantidade de Unidades Vendidas")

plt.show()

