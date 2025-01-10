import streamlit as st

# Simulação de produtos no e-commerce
products = [
    {"id": 1, "name": "Produto A", "price": 50.00},
    {"id": 2, "name": "Produto B", "price": 30.00},
    {"id": 3, "name": "Produto C", "price": 20.00},
    {"id": 4, "name": "Produto D", "price": 40.00},
]

# Função para exibir os produtos
def display_products():
    st.header("Produtos Disponíveis")
    for product in products:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(product["name"])
        with col2:
            st.write(f"R$ {product['price']:.2f}")
        with col3:
            if st.button("Adicionar ao Carrinho", key=f"add_{product['id']}"):
                add_to_cart(product)

# Função para inicializar o carrinho de compras
def initialize_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = []

# Função para adicionar produtos ao carrinho
def add_to_cart(product):
    st.session_state.cart.append(product)
    st.success(f"{product['name']} adicionado ao carrinho!")

# Função para exibir o carrinho de compras
def display_cart():
    st.header("Carrinho de Compras")
    if not st.session_state.cart:
        st.write("O carrinho está vazio.")
        return

    total = 0
    for item in st.session_state.cart:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(item["name"])
        with col2:
            st.write(f"R$ {item['price']:.2f}")
        total += item["price"]

    st.write("---")
    st.write(f"**Total: R$ {total:.2f}**")
    if st.button("Finalizar Compra"):
        finalize_purchase()

# Função para finalizar a compra
def finalize_purchase():
    st.session_state.cart = []
    st.success("Compra finalizada com sucesso!")

# Main
initialize_cart()
st.title("E-commerce com Streamlit")
menu = st.sidebar.selectbox("Menu", ["Produtos", "Carrinho"])

if menu == "Produtos":
    display_products()
elif menu == "Carrinho":
    display_cart()
