# Smoking Prediction using Machine Learning

Este repositório contém um Jupyter Notebook com uma análise exploratória e vários modelos de machine learning capazes de prever se um indivíduo é ou não fumador com base em bio-sinais como por exemplo peso, altura, idade, cáries dentárias, etc.

## Conteúdo

- `smoking_predictions.ipynb`: Notebook principal com o código que inclui as análises e as previsões, bem como gráficos que apoiam na visualização e comparação dos dados.
- `/original`: Pasta que contém os ficheiros .csv utilizados para treinar e testar os modelos de machine learning.
- `README.md`: Este ficheiro, com instruções de execução.

## Objetivo

O objetivo deste projeto é construir um modelo de classificação capaz de prever o status de fumo de um paciente (fumador ou não) a partir de atributos como:

- Idade, altura, peso e perímetro da cintura;
- Visão e audição;
- Pressão arterial (sistólica e diastólica);
- Níveis de açúcar no sangue;
- Perfil lipídico: colesterol total, triglicerídeos, HDL e LDL;
- Hemoglobina, proteína na urina, creatinina sérica;
- Enzimas hepáticas: AST, ALT, GTP;
- Presença de cáries dentárias;

##  Requisitos
Antes de executar o notebook, certificar que tem os seguintes elementos instalados e configurados:

### 1. Python 3
Se ainda não tem o Python instalado, pode instalá-lo aqui:

- **Windows / macOS**: [https://www.python.org/downloads/](https://www.python.org/downloads/)  
  > No instalador, **marque a opção “Add Python to PATH”** antes de continuar.

- **Linux**:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Depois de instalar, verificar a versão do Python com:

```bash
python --version
```

### 2. Ambiente virtual
Para evitar conflitos entre pacotes, criar e ativar um ambiente virtual:

```bash
python -m venv venv
```

- No Windows:
  ```bash
  venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalação dos pacotes necessários
Com o ambiente virtual ativo, instalar os pacotes usados no notebook:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

### 4. Jupyter Notebook
Para correr o notebook, iniciar o Jupyter com:

```bash
jupyter notebook
```
