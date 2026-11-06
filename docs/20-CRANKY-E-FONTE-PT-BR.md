# Primeiro lote do Cranky e correção do ê

Atualização de 2026-11-06 do piloto separado para USA v1.1 (Rev 1). Esta entrega corrige o tamanho do ê apontado pelo usuário na segunda fala do Funky e integra seis saudações do Cranky. O piloto passa a ter oito falas da Candy, quatro do Funky e seis do Cranky, além dos menus já localizados. A tradução do Cranky ainda é parcial.

## Correção solicitada pelo usuário

O gerador anterior removia uma linha do corpo do e ao reservar espaço para o circunflexo. Essa linha contém parte do traço inferior esquerdo; removê-la reduzia a altura aparente da letra. O slot do ê agora usa preserve_body: as seis linhas de corpo originais, nas posições 2–7 da célula, ficam idênticas às do e normal. O acento ocupa as duas linhas superiores, sem deslocar o corpo ou mudar a célula de 8 × 8 pixels.

A correção é compartilhada por Funky, Candy e Cranky. Nenhuma palavra foi trocada e os demais glifos permanecem iguais. Um teste de regressão confere todas as linhas do corpo; a mesma igualdade foi verificada com a fonte da ROM real em font-body-check.json.

Galeria atualizada do Funky: evidence/2026-11-06/pt-BR/cranky/funky-corrected/preview.html. Ela substitui a prévia anterior para revisar o ê. O retorno do usuário sobre a aparência corrigida continua pendente.

## Seis saudações do Cranky

| Contexto do texto | Redação em PT-BR |
| --- | --- |
| Perguntar por Diddy | Ei, Donkey! Cadê o Diddy? |
| Perguntar por Donks | Ei, Diddy! Cadê o Donks? |
| Surpresa com a visita | Ora, ora! Que surpresa ver você aqui hoje! |
| Reconhecer o progresso | Até que você foi bem chegando até aqui... |
| Recepção impaciente | Me achou, foi?! O que você quer?! |
| Comentário sobre Funky | Quem disse que estou aqui? Foi o Funky Kong irritante? |

Mantidos Donkey, Diddy, Donks e Funky Kong, incluindo o apelido Donks. As mensagens continuam curtas e conservam o tom provocador do Cranky. Dicas de fases, demais saudações, despedidas e falas de encerramento continuam em inglês nesta etapa.

Configuração em localization/pt-BR/cranky-pilot.json; gerador em scripts/generate_ptbr_cranky_pilot.py. Os seis registros em 0x3C07A4, 0x3C0935, 0x3C0990, 0x3C09BD, 0x3C09E8 e 0x3C0A14 mantêm 28, 27, 45, 43, 44 e 57 bytes, respectivamente. Preservados ponteiros, terminadores, número de linhas e paridades; o preenchimento acrescenta somente espaços laterais. Não foram acrescentados códigos de caracteres.

A galeria privada evidence/2026-11-06/pt-BR/cranky/verified-all/preview.html mostra cada texto selecionado pelo comparador no cenário do Cranky. Ela serve para revisar redação e leitura. As condições normais de seleção, inclusive a ausência de um dos Kongs nas duas primeiras saudações, não são reproduzidas pela galeria. O aplicativo mantém a seleção original.

## Validação e limites

- Build Release e 38 testes Python passaram, incluindo a altura do ê, preservação de nomes/apelido, tamanhos, linhas e ponteiros.
- As seis saudações do Cranky passaram na comparação individual: áudio completo e os 128 KiB de WRAM coincidiram com o original; diferenças de imagem apenas no diálogo. As seis capturas foram inspecionadas, sem cortes e com texto legível.
- Quatro falas do Funky conferidas novamente com a fonte corrigida: áudio completo e WRAM inteira iguais ao original, com diferenças visuais apenas na faixa do diálogo.
- Regressão da Candy nos quadros 4.350, 4.500 e 4.650: áudio igual, somente os ajustes de alinhamento já conhecidos na WRAM e diferenças visuais apenas no diálogo.
- Menus e entrada da fase passaram nos quadros 1.700, 2.300 e 4.800. Na fase, imagem, WRAM e áudio coincidiram com a versão habitual.
- Um ciclo Candy/reinício coincidiu entre aplicativo, runner e disco com saves de QA isolados; mesma SRAM do fixture anterior.
- Catálogo privado draft-05 passou nas verificações de inventário e nomes: 18 rascunhos históricos, 50 registros preservados e 278 ainda sem tradução. O aceite anterior da Candy permanece registrado separadamente.
- ROM e executável habitual preservados; saves pessoais não usados. Velocidade permanece em 60,0988 Hz. Nenhuma nova instalação.

O diagnóstico DKC_REV1_QA_CRANKY_MESSAGE existe somente no runner sem janela. Ele seleciona um dos seis endereços conhecidos na tabela inglesa de despedidas em 0x3C0144–0x3C0164, alcançada pela entrada EE no quadro 4.350 do roteiro de QA. Original e piloto recebem a mesma seleção. Isso permite inspecionar o renderizador sem alterar o arquivo da ROM ou a sequência do aplicativo. Uma tentativa inicial na tabela de saudações não selecionou o texto nesse checkpoint; somente verified-all/ reúne a execução final.

Revisão humana das novas prévias, condições normais de cada saudação, dicas restantes e campanha completa continuam pendentes.

## Reprodução

Fechar os processos de QA antes de recompilar para liberar os executáveis no Windows.

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-first-check --character cranky --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/funky-font-check --character funky --all-messages
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-font-check
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-menu-check
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/cranky-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

Evidências privadas em evidence/2026-11-06/pt-BR/cranky/: verified-all/, funky-corrected/, candy-regression/, menu-gameplay/, saves/, font-body-check.json, unit-tests.log e logs de build. Abrir **Testar DKC - PT-BR.cmd** para jogar no perfil próprio do piloto. O jogo habitual continua em **Jogar DKC.cmd**.

Próxima etapa: revisar a aparência corrigida do ê e as seis saudações; depois, ampliar o lote do Cranky com dicas verificadas em contexto.
