"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header
from langsmith import Client

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    # Verifica se temos credenciais mínimas
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not os.getenv("LANGSMITH_API_KEY") or not username:
        print("⚠️  LANGSMITH_API_KEY ou USERNAME_LANGSMITH_HUB não configurados. Pulando push para LangSmith.")
        return False

    # Criar objeto ChatPromptTemplate a partir do YAML
    inner = prompt_data
    if len(prompt_data) == 1 and isinstance(next(iter(prompt_data.values())), dict):
        inner = next(iter(prompt_data.values()))

    try:
        system = inner.get("system_prompt", "")
        user = inner.get("user_prompt", "{bug_report}")
        messages = [("system", system), ("user", user)]
        
        prompt_obj = ChatPromptTemplate.from_messages(messages)

        client = Client()
        print(f"Enviando prompt para LangSmith: {prompt_name}")

        commit = client.push_prompt(
            prompt_identifier=prompt_name,
            object=prompt_obj,
            description=inner.get("description", "Prompt otimizado (v2)"),
            tags=inner.get("tags", [])
        )

        print(f"✓ Push realizado. Commit: {commit}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    # Aceita tanto o dicionário direto quanto o conteúdo aninhado (key -> dict)
    inner = prompt_data
    if len(prompt_data) == 1 and isinstance(next(iter(prompt_data.values())), dict):
        inner = next(iter(prompt_data.values()))

    from utils import validate_prompt_structure
    return validate_prompt_structure(inner)


def main():
    """Função principal"""
    print_section_header("PUSH PROMPTS PARA LANGSMITH")

    yaml_path = "prompts/bug_to_user_story_v2.yml"
    data = load_yaml(yaml_path)

    if not data:
        print(f"❌ Não foi possível carregar o arquivo: {yaml_path}")
        return 1

    is_valid, errors = validate_prompt(data)
    if not is_valid:
        print("❌ Validação do prompt falhou:")
        for e in errors:
            print(f"   - {e}")
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    if not username:
        print("⚠️  USERNAME_LANGSMITH_HUB não configurado no .env. Configure antes de fazer push.")
        # Não é crítico para gerar o arquivo localmente
        return 1

    prompt_name = f"{username}/bug_to_user_story_v2"

    pushed = push_prompt_to_langsmith(prompt_name, data)
    if pushed:
        print("✓ Prompt enviado com sucesso")
        return 0
    else:
        print("⚠️  Push não realizado (ver mensagens acima).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
