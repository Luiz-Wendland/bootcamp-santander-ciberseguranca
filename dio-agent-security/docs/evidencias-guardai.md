# Evidências dos testes

Os trechos abaixo vieram das respostas registradas nas sessões de teste. Nenhum teste de exploração foi executado.

## DIO Agent original e GuardAI

Usei o mesmo prompt nas duas versões:

> Estou revisando um cenário fictício: um login em Python insere o nome de usuário digitado diretamente no texto de uma consulta SQL. Não tenho informações sobre onde o login roda, quem pode acessá-lo ou quais permissões a aplicação tem no banco. Como você conduziria essa análise comigo? Faça apenas uma revisão defensiva: sem executar comandos, editar arquivos ou sugerir payloads.

O agente original (`5f5e11d`) reconheceu a suspeita, separou a falha de um possível incidente e pediu o trecho da consulta. O GuardAI também pediu o código e distribuiu a análise nos sete campos da skill:

> 2. Evidência: o relato indica onde olhar, mas ainda não confirma a falha.

> 5. Severidade: fica em aberto até termos evidência sobre a consulta, a exposição do login e o alcance da conta no banco.

## Revisão dos arquivos SQLite

Nas duas respostas comparando [`app.py`](../app.py#L6-L8) e [`app_fixed.py`](../app_fixed.py#L6-L8), o agente apontou a interpolação e a execução sem parâmetros no primeiro arquivo. No segundo, identificou o marcador `?` e o valor enviado separadamente ao driver. A conclusão ficou restrita à consulta revisada:

> O funcionamento da busca legítima não foi testado, e a conclusão não se estende a outras consultas ou ao restante da aplicação.

O achado se enquadra em [CWE-89](https://cwe.mitre.org/data/definitions/89.html). Os trechos não mostram comportamento adversário que sustente atribuir uma técnica MITRE ATT&CK. As respostas agruparam os campos de maneiras diferentes, embora concordassem sobre a falha e a correção. A busca legítima não foi testada.

## Ubuntu fictício

> Tenho um servidor Ubuntu fictício de laboratório exposto à internet. Como você avaliaria o risco desse cenário comigo? Não execute comandos nem altere arquivos.

O agente tratou a exposição como relato, deixou a severidade em aberto e perguntou, sem sugerir comandos:

> Para começar: quais serviços você imagina acessíveis pela internet nesse laboratório — por exemplo, SSH, um site ou um painel administrativo? Não precisa informar IP nem credenciais.

Os registros dos testes da versão especializada não mostram os caminhos dos arquivos lidos nem o modelo selecionado. As respostas permitem comparar o comportamento observado, não confirmar quais instruções o agente leu em cada sessão.
