"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        if not prompts:
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml não encontrado")

        key = next(iter(prompts.keys()))
        prompt = prompts[key]

        assert 'system_prompt' in prompt
        assert isinstance(prompt['system_prompt'], str)
        assert prompt['system_prompt'].strip() != ''

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        if not prompts:
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml não encontrado")

        key = next(iter(prompts.keys()))
        prompt = prompts[key]

        system = prompt.get('system_prompt', '') or ''
        system_l = system.lower()

        assert ('você' in system_l) or ('you are' in system_l) or ('product manager' in system_l)

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        if not prompts:
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml não encontrado")

        key = next(iter(prompts.keys()))
        prompt = prompts[key]

        text = (prompt.get('system_prompt', '') + ' ' + prompt.get('user_prompt', '')).lower()

        assert ('markdown' in text) or ('user story' in text) or ('user-story' in text)

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        if not prompts:
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml não encontrado")

        key = next(iter(prompts.keys()))
        prompt = prompts[key]
        # Nos prompts atuais, os exemplos estão incluídos como texto dentro de `system_prompt`
        system = prompt.get('system_prompt', '') or ''
        assert 'EXEMPLO' in system, "Nenhum exemplo de few-shot encontrado em `system_prompt`"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        if not prompts:
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml não encontrado")

        key = next(iter(prompts.keys()))
        prompt = prompts[key]

        import re
        combined = yaml.dump(prompt)
        # Detecta placeholders explícitos: [TODO] (qualquer case) ou TODO em maiúsculas isolado
        has_bracketed = re.search(r'\[ *TODO *\]', combined, re.IGNORECASE)
        has_upper_todo = re.search(r'\bTODO\b', combined)
        assert not (has_bracketed or has_upper_todo), "Encontrado placeholder TODO no prompt"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        if not prompts:
            pytest.skip("Arquivo prompts/bug_to_user_story_v2.yml não encontrado")

        key = next(iter(prompts.keys()))
        prompt = prompts[key]

        techniques = prompt.get('techniques_applied', [])
        assert isinstance(techniques, list)
        assert len(techniques) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])