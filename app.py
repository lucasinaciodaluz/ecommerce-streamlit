import streamlit as st
import stripe
import os

# Configuração do Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'chave_secreta_padrao')

# Simulação de produtos no e-commerce
products = [
    {"id": 1, "name": "Produto A", "price": 50.00, "image": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='blue'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='14'>Produto A</text></svg>"},
    {"id": 2, "name": "Produto B", "price": 30.00, "image": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='green'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='14'>Produto B</text></svg>"},
    {"id": 3, "name": "Produto C", "price": 20.00, "image": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='red'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='14'>Produto C</text></svg>"},
    {"id": 4, "name": "Produto D", "price": 40.00, "image": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='purple'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='white' font-size='14'>Produto D</text></svg>"},
]

# Função para exibir os produtos
def display_products():
    st.header("Produtos Disponíveis")
    for product in products:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image(product["image"], width=100)
        with col2:
            st.write(product["name"])
            st.write(f"R$ {product['price']:.2f}")
        with col3:
            if st.button("Adicionar ao Carrinho", key=f"add_{product['id']}"):
                add_to_cart(product)

# Função para inicializar o carrinho de compras
def initialize_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

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
    line_items = []
    for item in st.session_state.cart:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image(item["image"], width=100)
        with col2:
            st.write(item["name"])
            st.write(f"R$ {item['price']:.2f}")
        total += item["price"]
        line_items.append({
            'price_data': {
                'currency': 'brl',
                'product_data': {'name': item['name']},
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': 1,
        })

    st.write("---")
    st.write(f"**Total: R$ {total:.2f}**")

    if st.button("Finalizar Compra"):
        create_stripe_checkout_session(line_items)

# Função para criar a sessão de checkout do Stripe
def create_stripe_checkout_session(line_items):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8501',  # Substitua pelo URL de sucesso real
            cancel_url='http://localhost:8501',   # Substitua pelo URL de cancelamento real
        )
        st.success("Redirecionando para o pagamento...")
        st.markdown(f"[Clique aqui para pagar]({session.url})", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao criar sessão de pagamento: {e}")

# Função para tela de login
def login_screen():
    st.header("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username == "admin" and password == "123":
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# Função para exibir o ícone do carrinho com contagem
def display_cart_icon():
    cart_count = len(st.session_state.cart)
    st.sidebar.markdown(f"<div style='display: flex; align-items: center;'>"
                        f"<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' fill='currentColor' class='bi bi-cart' viewBox='0 0 16 16'>"
                        f"<path d='M0 1.5A.5.5 0 0 1 .5 1h1a.5.5 0 0 1 .485.379L2.89 5H14.5a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 13 14H4a.5.5 0 0 1-.491-.408L1.01 2H.5a.5.5 0 0 1-.5-.5zm3.14 4l1.313 7h7.093l1.313-7H3.14zM5 12a1 1 0 1 0 0 2 1 1 0 0 0 0-2zm6 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2z'/>"
                        f"</svg>"
                        f"<span style='margin-left: 8px;'>Itens: {cart_count}</span></div>", unsafe_allow_html=True)

# Main
initialize_cart()
st.title("E-commerce com Streamlit")

if not st.session_state.logged_in:
    login_screen()
else:
    display_cart_icon()
    menu = st.sidebar.selectbox("Menu", ["Produtos", "Carrinho"])
    if menu == "Produtos":
        display_products()
    elif menu == "Carrinho":
        display_cart()
