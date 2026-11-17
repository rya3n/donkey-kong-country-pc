# Donkey Kong Country — Port para PC

## Retomada

- Consulte [as etapas e pendências](docs/06-ETAPAS-E-PENDENCIAS.md), [a validação da campanha](docs/32-CAMPANHA-PT-BR-AUDIO-E-PROGRESSO.md) e o [changelog](CHANGELOG.md). Cruze o último marco com a branch e o estado do repositório antes de continuar.
- Quando o Notion estiver disponível, abra a página do projeto Donkey Kong Country — Port para PC. Consulte o guia de retomada, o roadmap, a Central de Bugs e o registro de decisões conforme a tarefa.
- Na publicação de um marco, atualize o roteiro, a validação e as pendências aplicáveis. Vincule o commit confirmado ao registro no Notion e indique o próximo passo verificável.

## Trabalho e validação

- Use o alvo Windows USA v1.1 (Rev 1) com a ROM local e as ferramentas descritas no [guia de ambiente](docs/04-AMBIENTE-E-REPRODUCAO.md). Mantenha instalações do projeto no E: conforme a preferência do usuário.
- Em mudanças de gameplay, preserve a cadência alvo de 60,0988 Hz. Para validar o avanço da campanha, use um perfil de QA separado e registre a entrada, a saída, a seleção final do mapa e o alcance real do teste.
- Utilize `python -m unittest discover -s tests` para a suíte Python. Se houver mudança de comportamento no port, execute também os testes nativos ou o cenário interativo aplicável do [plano de validação](docs/05-VALIDACAO.md).
- Preserve nomes e contexto importantes do jogo na localização. Sustente a conclusão de PT-BR com a revisão em contexto, incluindo as telas e os créditos previstos.
- Proteja ROMs, saves pessoais, credenciais e evidências privadas. Publique código, documentação e receitas apropriadas ao repositório. Confira o diff e os arquivos preparados antes de publicar.
- O [escopo](docs/01-VISAO-E-ESCOPO.md) e a validação definem quando a entrega está pronta. Registre melhorias opcionais como manutenção futura. A revisão geral do volume de arquivos fica para depois da recompilação.
