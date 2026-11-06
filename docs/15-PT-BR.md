# Preparação da tradução PT-BR

Iniciada em 2026-11-05 por autorização do usuário, com a orientação de preservar nomes importantes e o contexto do jogo. Esta etapa produz inventário, glossário e rascunhos. A campanha completa permanece pendente; o executável jogável não recebeu alterações de texto.

Atualização posterior: os menus foram localizados e um build experimental separado recebeu cinco rótulos gráficos em PT-BR. O executável habitual e os 12 rascunhos de falas permanecem como antes. Ver [Piloto dos menus](16-PILOTO-PT-BR.md). O relatório abaixo registra a extração inicial.

## Regra editorial

- Manter nomes próprios de personagens, inimigos, animais, lugares, fases, marcas e pessoas dos créditos. Preservar grafia, identidade e pontuação; não substituir por uma tradução literal.
- Preservar os nomes completos do mapa, incluindo os locais de serviço. O termo genérico “ponto de salvamento” pode aparecer numa instrução sem renomear Candy's Save Point.
- Traduzir menus, mensagens, instruções e falas com português brasileiro natural, mantendo a informação de gameplay e a personalidade de quem fala.
- Manter apelidos e termos ambíguos enquanto o contexto não estiver revisto. Não expandir uma abreviação, inventar parentesco ou trocar uma referência para facilitar o encaixe.
- Rever mensagens consecutivas em conjunto. Uma frase pode continuar no próximo registro; revisar uma entrada isolada pode mudar o sentido.
- Usar acentos corretos nos rascunhos. A fonte e o espaço disponível precisam ser verificados antes de integrar a tradução; remover acentos não é a solução padrão.

Exemplos protegidos: Donkey Kong, Diddy Kong, Cranky Kong, Candy Kong, Funky Kong, K. Rool, Rambi, Enguarde, Expresso, Winky, Squawks, Kremlings, DK, KONG e TNT. Nomes como Jungle Hijinxs permanecem originais. A política inicial está em localization/pt-BR/policy.json; os rótulos completos do mapa também são protegidos pelo verificador do catálogo.

Termos genéricos iniciais: save → salvar; lives → vidas; level → fase; bonus room → sala de bônus; jump → pular. Essa lista nunca se sobrepõe a um nome próprio completo.

## Inventário inicial da Rev 1

O leitor próprio confere tamanho e SHA-256 exatos antes de ler a ROM. Os limites abaixo foram conferidos nos dados da Rev 1. A referência de disassembly é da v1.0: não foram importados seus offsets como se fossem equivalentes. Por exemplo, o bloco de créditos da nossa entrada começa em 0x01EFFC, enquanto a referência identifica o início em 0x01EFDE.

| Região | Intervalo de arquivo, fim exclusivo | Registros | Conteúdo observado |
| --- | --- | --- | --- |
| map_names_en | 0x38A50B–0x38A7EA | 50 | Rótulos em inglês do mapa, incluindo o marcador ERROR; preservar nesta etapa |
| cast_en | 0x01DFD5–0x01E1BC | 47 | Nomes, títulos e falas curtas da apresentação do elenco |
| credits_en | 0x01EFFC–0x01F405 | 32 | Créditos, nomes e brincadeiras do encerramento |
| dialogue_en | 0x3C03C8–0x3C35CA | 217 | Bloco de falas em inglês |
| **Total inicial** | **Quatro regiões** | **346** | **Cobertura parcial do texto do jogo** |

Nessas regiões, o bit alto marca o último caractere de uma linha; parte dos blocos separa mensagens com zero. O leitor mantém linhas, offsets e comprimentos originais. Um caractere/controle desconhecido ou um limite incompleto interrompe a leitura; não é descartado silenciosamente.

Seleção de arquivo, modos de jogadores, texto desenhado como gráfico, instruções fora desses blocos e eventuais duplicatas continuam por localizar. Os 346 registros não constituem um inventário completo do jogo.

## Trabalho realizado

- Extraído catálogo privado de 346 registros, com identidade da ROM e campos de revisão.
- Criados 12 rascunhos editoriais: duas saudações de Cranky, quatro falas de Funky e seis falas de Candy. São propostas de texto, ainda sem revisão em tela, quebras de linha ou codificação de acentos aprovadas.
- Os 50 rótulos do mapa ficaram preservados; 284 registros permanecem sem tradução e 12 estão em rascunho.
- Verificador passou no catálogo real: IDs, fonte, offsets e nomes protegidos preservados. Os seis testes com textos sintéticos passaram, incluindo rejeição de nome alterado, fonte modificada e aprovação indevida do rascunho.
- Hashes da ROM e do executável permaneceram iguais. O leitor não escreve na ROM; nenhum save foi aberto e nenhuma dependência foi instalada.

O verificador estrutural não julga fidelidade semântica, humor ou naturalidade. Cada fala exige revisão no contexto, e nomes novos devem ser incorporados ao glossário conforme forem identificados.

## Reprodução local

```powershell
python scripts/inventory_rev1_text.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out experimental/usa-rev1/pt-BR/catalog-initial.json
python scripts/check_ptbr_catalog.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --original experimental/usa-rev1/pt-BR/catalog-initial.json --draft experimental/usa-rev1/pt-BR/catalog-draft-01.json
python -m unittest discover -s tests -p test_ptbr_review.py -v
```

O inventário recusa sobrescrever um arquivo existente. Para nova extração, escolher outro nome dentro de experimental/ ou evidence/, sem substituir o catálogo já editado. A ferramenta de inventário cria a fonte inicial; os rascunhos são trabalho editorial separado. Catálogos com textos originais e traduções ficam somente nas pastas privadas ignoradas; o repositório publica leitor, verificações, política e relatório.

Evidências desta execução: evidence/2026-11-05/pt-BR/. Catálogos locais: experimental/usa-rev1/pt-BR/. Não há patch de tradução ou alteração no runtime nesta entrega.

## Próxima etapa técnica

Localizar menus e suas tabelas/fontes na Rev 1, verificar os glifos de PT-BR e o espaço por linha, e definir como integrar dados traduzidos sem alterar endereços de código ou a identidade da ROM original. Depois, realizar um piloto visual separado, comparar execução, áudio e saves, e revisar as falas em tela. A cobertura de campanha continua registrada no plano de validação; a preparação editorial não a aprova automaticamente.

Referência estrutural consultada localmente: [disassembly de Yoshifanatic1, revisão c2080f4](https://github.com/Yoshifanatic1/Donkey-Kong-Country-1-Disassembly/tree/c2080f40469c716923f550706509a0d354229841). A referência declara suporte a USA v1.0 e licença GPLv3; nenhum trecho de sua implementação foi copiado para o leitor próprio. A extração desta etapa usa exclusivamente a ROM Rev 1 conferida.
