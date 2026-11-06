# Piloto das primeiras falas da Candy

Atualização de 2026-11-06 do build PT-BR separado. As duas mensagens de apresentação e de instrução de salvamento da Candy foram traduzidas. O nome Candy Kong, a placa Candy's Save Point e as ações do jogo permanecem originais. A tradução completa continua pendente.

## Testar

- **Testar falas da Candy.cmd:** prévia que percorre o boot de diagnóstico e entra diretamente na Candy. Não carrega nem grava saves pessoais em disco. Aguarde o ciclo de apresentação e instrução para ver as duas mensagens.
- **Testar DKC - PT-BR.cmd:** inicia o piloto pelo menu normal, com progresso próprio em data/usa-rev1-ptbr-pilot/saves/. Use essa abertura para jogar e salvar na Candy normalmente.
- **Jogar DKC.cmd:** continua abrindo a versão habitual. Seu executável e seus saves não foram substituídos.

Controles, F6 e F11 continuam iguais. A prévia é um diagnóstico de leitura, não uma retomada do progresso da campanha nem um save state. Para recompilar, usar scripts/build_ptbr_pilot.ps1 com o piloto fechado.

## Texto integrado

Apresentação, em duas linhas:

```text
Olá!  Sou a Candy Kong!
Você pode salvar aqui!
```

Instrução, em três linhas:

```text
Para salvar seu jogo atual,
pule no meu barril giratório
de salvamento!
```

A apresentação conserva a saudação, a identidade e o significado de ponto de salvamento. A instrução continua dizendo para pular no barril giratório para salvar o jogo atual. A quebra de linha e o preenchimento lateral são definidos pela largura disponível; não houve troca de nomes para encaixar o texto.

## Integração e fonte

As mensagens ocupam os mesmos 46 e 72 bytes, incluindo terminadores. Mantidos os dois/três finais de linha, o zero final e os ponteiros em 0x3C0354. A primeira mensagem tem dois espaços após a saudação; a primeira linha da instrução tem preenchimento equilibrado nas laterais no arquivo de dados. Não houve realocação de texto, expansão da ROM ou alteração de código do cartucho/AOT.

A fonte do diálogo é de 2 bpp, diferente da fonte de 4 bpp dos menus. O endereço 0x29D6DC e seu carregamento na Rev 1 foram conferidos. Foram construídos á, ê e ó a partir dos glifos existentes, mantendo contorno e célula de 8×8 pixels. Os códigos 0x5B–0x5D estavam ausentes nos quatro blocos em inglês do inventário e foram reservados para esses três caracteres. Não é uma extensão multilíngue: outros idiomas, caracteres e telas ainda precisam de revisão antes de ampliar a fonte.

O piloto aplica dez regiões de dados na cópia em memória: as cinco regiões dos menus, as duas falas e três glifos de 16 bytes. O arquivo de ROM original não é escrito. O manifesto e o log registram o hash do conjunto de alterações para detectar executável com dados gerados antigos.

## Verificações

| Verificação | Resultado e limite |
| --- | --- |
| Build e testes | Build Release e 20 testes Python passaram, incluindo nomes, limites, tamanhos, ponteiros, glifos e encoding |
| Capturas nativas | Mensagens e acentos inspecionados em 4.350 e 4.650 quadros; também conferido o fade no quadro 4.500 |
| Imagem | Diferenças restritas à faixa do diálogo; Candy, Donkey, barril, placa e cenário iguais fora dessa faixa |
| WRAM | Restante dos 128 KiB idêntico; diferenças apenas nas palavras de alinhamento horizontal de texto em 0x068D/0x0697/0x06A1 |
| Execução e áudio | Cadeia completa de áudio idêntica; 19 instruções interpretadas adicionais no caminho de centralização do texto, sem alteração no relógio de 60,0988 Hz |
| Menus e entrada da fase | Regressão de 1.700/2.300/4.800 quadros passou; imagem da fase, WRAM e áudio coincidiram com a versão habitual |
| Save e reinício | Um par Candy/reinício passou entre aplicativo, runner e disco em perfis exclusivos de QA |
| Prévia de acesso direto | Janela oculta em --candy coincidiu com o runner em imagem/WRAM após a preparação; saves desativados e arquivos pessoais/backup preservados |
| Dados e versão habitual | Hashes da ROM e do executável habitual preservados; nenhuma instalação nova |

Não se exige igualdade do hash inteiro de WRAM durante uma fala traduzida: a rotina original calcula o alinhamento usando as novas linhas. A comparação é byte a byte e aceita apenas os campos de alinhamento identificados. No quadro 4.350 e no fade 4.500 mudam 0x06A1–0x06A2; na instrução 4.650 mudam 0x068D–0x068E e 0x0697–0x0698. Os demais bytes devem coincidir. O verificador rejeita mudanças fora desses campos e diferenças visuais fora da faixa do diálogo.

Os checkpoints foram preparados por entrada de diagnóstico, não por uma campanha completa. Capturas são do framebuffer nativo e a prévia automatizada usou janela oculta; legibilidade no monitor e aceite das falas ainda dependem do teste humano.

## Reprodução

```powershell
./scripts/build_rev1.ps1 -HeadlessOnly
./scripts/build_ptbr_pilot.ps1
python -m unittest discover -s tests -p 'test_ptbr*.py' -v
python scripts/verify_ptbr_candy_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-dialogue-check
python scripts/verify_ptbr_menu_pilot.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-menu-regression
python scripts/verify_rev1_saves.py --rom 'Donkey Kong Country (USA) (Rev 1).sfc' --out evidence/candy-save-check --build-dir build/ptbr-pilot --desktop-name DKC-Rev1-PTBR-Piloto.exe --repeats 1
```

HeadlessOnly recompila apenas o comparador sem janela, preservando o executável habitual. A opção DKC_REV1_WRAM_DUMP, exclusiva do runner sem janela, grava a memória final somente quando um caminho explícito é fornecido; os verificadores usam evidence/. Ela não modifica a execução do jogo.

Evidências privadas em evidence/2026-11-06/pt-BR/candy/, incluindo final-dialogue/, verified-menu-gameplay/, saves/, preview/, unit-tests.log e build.log. O catálogo privado catalog-draft-02.json registra a redação integrada; duas das 12 falas do lote inicial estão no piloto, com aceite humano pendente. As outras dez continuam em rascunho fora do runtime.

Próxima etapa: revisar a leitura e o tom destas mensagens com o usuário e avançar para as outras falas da Candy, reaproveitando o glossário e ampliando os acentos somente quando necessários e verificados. Campanha e tradução integral continuam com cobertura pendente.
