import os
import smtplib
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv


def carregar_configuracoes():
    """Carrega as variáveis do arquivo .env."""
    print("Carregando configurações do .env...")
    load_dotenv()

    config = {
        "smtp_server": os.getenv("SMTP_SERVER"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "smtp_user": os.getenv("SMTP_USER"),
        "smtp_password": os.getenv("SMTP_PASSWORD"),
        "from_email": os.getenv("FROM_EMAIL"),
    }

    faltando = [k for k, v in config.items() if not v]
    if faltando:
        raise ValueError(f"Estão faltando variáveis no .env: {', '.join(faltando)}")

    print("Config carregada:")
    for k, v in config.items():
        # nunca mostrar a senha
        mascara = v if "password" not in k.lower() else "***"
        print(f"  {k} = {mascara}")

    return config


def enviar_email_com_anexo(para_email: str, assunto: str, corpo: str, caminho_anexo: str):
    """Envia um e-mail com anexo para o cliente."""
    config = carregar_configuracoes()

    print(f"\nMontando mensagem para: {para_email}")

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = config["from_email"]
    msg["To"] = para_email
    msg.set_content(corpo)

    # Anexar arquivo, se existir
    if caminho_anexo:
        if os.path.isfile(caminho_anexo):
            print(f"Incluindo anexo: {caminho_anexo}")
            tipo_mime, _ = mimetypes.guess_type(caminho_anexo)
            if tipo_mime is None:
                tipo_mime = "application/octet-stream"

            tipo_principal, subtipo = tipo_mime.split("/", 1)

            with open(caminho_anexo, "rb") as f:
                dados = f.read()
                nome_arquivo = os.path.basename(caminho_anexo)
                msg.add_attachment(
                    dados,
                    maintype=tipo_principal,
                    subtype=subtipo,
                    filename=nome_arquivo,
                )
        else:
            print(f"Aviso: anexo '{caminho_anexo}' não encontrado. Enviando sem anexo.")
    else:
        print("Nenhum anexo configurado.")

    print("\nConectando ao servidor SMTP...")

    try:
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.set_debuglevel(1)  # mostra comunicação com o servidor
            server.starttls()
            print("Autenticando no servidor SMTP...")
            server.login(config["smtp_user"], config["smtp_password"])
            print("Enviando mensagem...")
            server.send_message(msg)
        print("\nE-mail ENVIADO com sucesso.")
    except Exception as e:
        print("\nERRO AO ENVIAR E-MAIL:")
        print(type(e).__name__, "-", e)

from db import criar_tabela, inserir_cliente, listar_clientes
def menu():
    print("\n=== LembreteEmail ===")
    print("1 - Cadastrar cliente")
    print("2 - Listar clientes")
    print("3 - Enviar e-mail de lembrete para um cliente (ID)")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")
    return opcao.strip()


def fluxo_cadastrar_cliente():
    print("\n--- Cadastro de Cliente ---")
    nome = input("Nome do cliente: ").strip()
    email = input("E-mail do cliente: ").strip()
    data_vencimento = input("Data de vencimento (AAAA-MM-DD): ").strip()
    dias_antes = int(input("Enviar lembrete quantos dias antes do vencimento? ").strip())
    horario_envio = input("Horário do envio (HH:MM, 24h): ").strip()
    caminho_boleto = input("Caminho completo do arquivo do boleto (PDF): ").strip()

    inserir_cliente(nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto)
    print("Cliente cadastrado com sucesso!")


def fluxo_listar_clientes():
    print("\n--- Clientes Cadastrados ---")
    clientes = listar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    for cli in clientes:
        (cli_id, nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto) = cli
        print(
            f"ID: {cli_id} | Nome: {nome} | Email: {email} | "
            f"Vencimento: {data_vencimento} | Dias antes: {dias_antes} | "
            f"Horário: {horario_envio} | Boleto: {caminho_boleto}"
        )


def fluxo_enviar_para_cliente():
    from datetime import datetime

    print("\n--- Enviar lembrete para cliente ---")
    try:
        cliente_id = int(input("Informe o ID do cliente: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    clientes = listar_clientes()
    cliente_escolhido = None
    for cli in clientes:
        if cli[0] == cliente_id:
            cliente_escolhido = cli
            break

    if not cliente_escolhido:
        print("Cliente não encontrado.")
        return

    (cli_id, nome, email, data_vencimento, dias_antes, horario_envio, caminho_boleto) = cliente_escolhido

    assunto = f"Lembrete de pagamento - vencimento em {data_vencimento}"
    corpo = (
        f"Olá {nome},\n\n"
        f"Este é um lembrete de que seu boleto vence em {data_vencimento}.\n"
        f"Qualquer dúvida, entre em contato.\n\n"
        f"Att,\nSeu Sistema de Lembretes"
    )

    print(f"\nEnviando e-mail para {email}...")
    enviar_email_com_anexo(email, assunto, corpo, caminho_boleto)
    print("Fluxo de envio finalizado.")


if __name__ == "__main__":
    criar_tabela()  # garante que a tabela existe

    while True:
        opcao = menu()
        if opcao == "1":
            fluxo_cadastrar_cliente()
        elif opcao == "2":
            fluxo_listar_clientes()
        elif opcao == "3":
            fluxo_enviar_para_cliente()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

    # se quiser testar sem anexo, deixe vazio: ""
    caminho_boleto = ""  # ou r"C:\caminho\para\um\arquivo.pdf"

    print("Iniciando envio de e-mail de teste...")
    enviar_email_com_anexo(email_cliente, assunto, corpo, caminho_boleto)
    print("Programa finalizado.")
