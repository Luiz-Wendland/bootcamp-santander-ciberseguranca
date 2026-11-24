# Medusa no Metasploitable 2: FTP e SMB

## Ambiente

Usei o Kali (`192.168.56.102`) e o Metasploitable 2 (`192.168.56.101`) numa rede host-only do VirtualBox. Testei a senha padrão no FTP e no SMB com o Medusa v2.3.

## Reconhecimento

```bash
nmap -sV 192.168.56.101
```

A varredura mostrou o vsftpd 2.3.4 na porta 21 e o Samba nas portas 139 e 445.

## FTP

Criei uma lista temporária com três usuários e fiz o teste com o módulo `ftp`. O Medusa usou o nome do primeiro usuário como senha. O login funcionou e o teste parou ali.

Depois, testei o acesso pelo cliente FTP:

```bash
ftp 192.168.56.101
```

```text
220 (vsFTPd 2.3.4)
[...]
230 Login successful.
```

Pelo Kali, tentei entrar na mesma conta com uma senha errada e depois com a correta. No servidor, acompanhei o log:

```bash
sudo tail -n 0 -f /var/log/vsftpd.log
```

Trecho de 23/11/2026 (horário da VM, conta omitida):

```text
18:58:01 [...] [conta omitida] FAIL LOGIN: Client "192.168.56.102"
18:58:17 [...] [conta omitida] OK LOGIN: Client "192.168.56.102"
```

## SMB

Comecei verificando as versões do SMB e as permissões dos compartilhamentos:

```bash
nmap -p139,445 --script smb-protocols,smb-enum-shares 192.168.56.101
```

```text
[...]
|_    NT LM 0.12 (SMBv1) [dangerous, but default]
[...]
|   \\192.168.56.101\tmp:
[...]
|_    Anonymous access: READ/WRITE
```

```bash
smbclient -L 192.168.56.101 -N
```

```text
Anonymous login successful
[...]
        tmp             Disk      oh noes!
```

Usei o módulo `smbnt` para testar o mesmo usuário e senha. O Medusa indicou acesso a `ADMIN$` logo na primeira tentativa:

```text
ACCOUNT FOUND: [smbnt] [...] [SUCCESS (ADMIN$ - Access Allowed)]
```

## Mitigações

| Problema | Como corrigir |
| --- | --- |
| Senha padrão funcionando no FTP e no SMB | Remover contas padrão que não estejam em uso e trocar as senhas das demais por senhas únicas. Limitar tentativas ajuda contra repetições, mas não impede um acerto de primeira. |
| Listagem anônima e permissões de leitura e escrita indicadas em `tmp` | Desativar o acesso de convidado e restringir as permissões de cada compartilhamento. |
| SMBv1 habilitado | Atualizar o Samba e desativar o SMBv1. A troca das senhas continua necessária. |
