import streamlit as st
import requests
import pandas as pd
from datetime import datetime  # Adicionando a importação do datetime

# Configuração da página
st.set_page_config(layout="wide")
st.title("Gerenciamento de Produtos e Estoque")

# URL do backend (ajuste conforme necessário)
BASE_URL = "http://backend:8000"

# Função para exibir mensagens de resposta
def show_response_message(response):
    if response.status_code == 200:
        st.success("Operação realizada com sucesso!")
    else:
        try:
            data = response.json()
            if "detail" in data:
                if isinstance(data["detail"], list):
                    errors = "\n".join([error["msg"] for error in data["detail"]])
                    st.error(f"Erro: {errors}")
                else:
                    st.error(f"Erro: {data['detail']}")
        except ValueError:
            st.error("Erro desconhecido. Não foi possível decodificar a resposta.")

# Adicionar Produto
with st.expander("Adicionar um Novo Produto"):
    with st.form("new_product"):
        name = st.text_input("Nome do Produto", value=st.session_state.get('name', ''))
        description = st.text_area("Descrição do Produto", value=st.session_state.get('description', ''))
        price = st.number_input("Preço", min_value=0.01, format="%f", value=st.session_state.get('price', 0.01))
        submit_button = st.form_submit_button("Adicionar Produto")

        if submit_button:
            response = requests.post(
                f"{BASE_URL}/products/",
                json={
                    "name": name,
                    "description": description,
                    "price": price,
                },
            )
            show_response_message(response)

            # Limpar os campos após adicionar o produto com sucesso
            if response.status_code == 200:
                st.session_state.name = ''
                st.session_state.description = ''
                st.session_state.price = 0.01

# Visualizar Produtos
with st.expander("Visualizar Produtos"):
    if st.button("Exibir Todos os Produtos"):
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            df = pd.DataFrame(products)

            # Exibindo produtos
            df = df[[
                "id", "name", "description", "price", "created_at"
            ]]
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Obter Detalhes de um Produto
with st.expander("Obter Detalhes de um Produto"):
    get_id = st.number_input("ID do Produto", min_value=1, format="%d")
    if st.button("Buscar Produto"):
        response = requests.get(f"{BASE_URL}/products/{get_id}")
        if response.status_code == 200:
            product = response.json()
            df = pd.DataFrame([product])

            df = df[[
                "id", "name", "description", "price", "created_at"
            ]]
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Deletar Produto
with st.expander("Deletar Produto"):
    delete_id = st.number_input("ID do Produto para Deletar", min_value=1, format="%d")
    if st.button("Deletar Produto"):
        response = requests.delete(f"{BASE_URL}/products/{delete_id}")
        show_response_message(response)

# Atualizar Produto
with st.expander("Atualizar Produto"):
    with st.form("update_product"):
        update_id = st.number_input("ID do Produto", min_value=1, format="%d")
        new_name = st.text_input("Novo Nome do Produto")
        new_description = st.text_area("Nova Descrição do Produto")
        new_price = st.number_input(
            "Novo Preço",
            min_value=0.01,
            format="%f",
        )

        update_button = st.form_submit_button("Atualizar Produto")

        if update_button:
            update_data = {}
            if new_name:
                update_data["name"] = new_name
            if new_description:
                update_data["description"] = new_description
            if new_price > 0:
                update_data["price"] = new_price

            if update_data:
                response = requests.put(
                    f"{BASE_URL}/products/{update_id}", json=update_data
                )
                show_response_message(response)

                # Limpar os campos após atualização bem-sucedida
                if response.status_code == 200:
                    st.session_state.new_name = ''
                    st.session_state.new_description = ''
                    st.session_state.new_price = 0.01
            else:
                st.error("Nenhuma informação fornecida para atualização")

# Inicializa a lista de itens no session_state, se não existir
if 'items' not in st.session_state:
    st.session_state.items = []

# Adicionar Movimentação de Estoque
with st.expander("Adicionar Movimentação de Estoque"):
    # Inicializa a lista de itens no session_state, se não existir
    if 'items' not in st.session_state:
        st.session_state['items'] = []

    # Formulário para selecionar tipo de movimentação e data
    movement_type = st.selectbox("Tipo de Movimentação", ["entrada", "saída"])
    movement_date = st.date_input("Data da Movimentação", datetime.now())

    # Formulário para adicionar itens
    with st.form("add_item_form", clear_on_submit=True):
        product_id = st.number_input("ID do Produto", min_value=1)
        quantity = st.number_input("Quantidade", min_value=1)
        add_item_button = st.form_submit_button("Adicionar Item")

        if add_item_button:
            if product_id and quantity:
                item = {"product_id": product_id, "quantity": quantity}
                st.session_state['items'].append(item)  # Adiciona o item à lista
                st.success(f"Item {product_id} adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos para adicionar o item.")

    # Exibir os itens adicionados
    if st.session_state['items']:
        st.write("Itens Adicionados:")
        for item in st.session_state['items']:
            st.write(f"Produto ID: {item['product_id']} | Quantidade: {item['quantity']}")

    # Submeter a movimentação de estoque
    if st.button("Adicionar Movimentação"):
        if st.session_state['items']:
            movement_data = {
                "type": movement_type,
                "movement_date": movement_date.isoformat(),
                "items": st.session_state['items']
            }

            # Enviar os dados para a API
            response = requests.post(
                f"{BASE_URL}/stock-movements/",
                json=movement_data
            )
            show_response_message(response)

            # Limpar a lista de itens após o envio bem-sucedido
            if response.status_code == 200:
                st.session_state['items'].clear()  # Limpa a lista de itens
        else:
            st.error("Por favor, adicione pelo menos um item à movimentação.")

# Visualizar Movimentações de Estoque
with st.expander("Visualizar Movimentações de Estoque"):
    if st.button("Exibir Movimentações de Estoque"):
        response = requests.get(f"{BASE_URL}/stock-movements/")
        if response.status_code == 200:
            movements = response.json()
            df = pd.DataFrame(movements)
            st.write(df.to_html(index=False), unsafe_allow_html=True)
        else:
            show_response_message(response)

# Consultar o Estoque de um Produto
with st.expander("Consultar Estoque de um Produto"):
    product_id = st.number_input("ID do Produto para Ver Estoque", min_value=1)
    if st.button("Ver Estoque"):
        response = requests.get(f"{BASE_URL}/products/{product_id}/stock")
        if response.status_code == 200:
            stock = response.json()
            st.write(stock)
        else:
            show_response_message(response)
