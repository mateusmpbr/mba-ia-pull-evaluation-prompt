"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Tenta puxar o prompt do LangSmith Hub. Se a variável `LANGSMITH_API_KEY`
    não estiver configurada ou o pull falhar, faz fallback para o arquivo
    local existente em `prompts/bug_to_user_story_v1.yml`.
    """
    print_section_header("PULL PROMPTS DO LANGSMITH")

    prompt_name = "leonanluppi/bug_to_user_story_v1"
    target_path = Path("prompts/bug_to_user_story_v1.yml")

    # Se já existe localmente, não precisa puxar nada
    if target_path.exists():
        print(f"✓ Prompt local já existe: {target_path}")
        return True

    # Tentar puxar do LangSmith se a chave estiver configurada
    if os.getenv("LANGSMITH_API_KEY"):
        try:
            print(f"Conectando ao LangSmith e puxando: {prompt_name}")
            prompt = hub.pull(prompt_name)

            # Tentar serializar para um YAML mínimo
            data = {
                "bug_to_user_story_v1": {
                    "description": getattr(prompt, "description", "Pulled from LangSmith"),
                    "system_prompt": getattr(prompt, "system_prompt", str(prompt)),
                    "user_prompt": "{bug_report}",
                    "version": "v1",
                }
            }

            saved = save_yaml(data, str(target_path))
            if saved:
                print(f"✓ Prompt salvo em: {target_path}")
                return True
            else:
                print("⚠️  Falha ao salvar o prompt puxado localmente")

        except Exception as e:
            print(f"⚠️  Erro ao puxar do LangSmith: {e}")

    print("❌ Não foi possível puxar o prompt do LangSmith e/ou arquivo local não existe.")
    print("   Verifique a variável LANGSMITH_API_KEY no .env ou crie o arquivo prompts/bug_to_user_story_v1.yml manualmente.")
    return False


def main():
    """Função principal"""
    print_section_header("EXECUTANDO PULL")

    success = pull_prompts_from_langsmith()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
