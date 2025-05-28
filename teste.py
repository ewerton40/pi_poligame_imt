import sys
import os
import traceback
# Garante que as pastas do projeto sejam encontradas
caminho_projeto = os.path.abspath(os.path.dirname(__file__))
if caminho_projeto not in sys.path:
    sys.path.append(caminho_projeto)

# Importa a tela de gerenciamento
try:
    from Telas.TelaGerenciamento import TelaGerenciamento
except ModuleNotFoundError as e:
    print("Erro durante a execução da tela:")
    traceback.print_exc()

if __name__ == '__main__':
    try:
        tela = TelaGerenciamento()
        tela.executar()
    except Exception as e:
        import traceback
        print("Erro durante a execução da tela:")
        traceback.print_exc()
