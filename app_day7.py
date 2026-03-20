import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(page_title="Order Application", layout="wide", initial_sidebar_state="expanded")

inventory = [
    {"item_id": 1, "name": "Espresso", "unit_price": 2.50, "stock": 40},
    {"item_id": 2, "name": "Latte", "unit_price": 4.25, "stock": 25},
    {"item_id": 3, "name": "Cold Brew", "unit_price": 3.75, "stock": 30},
    {"item_id": 4, "name": "Mocha", "unit_price": 4.50, "stock": 20},
    {"item_id": 5, "name": "Blueberry Muffin", "unit_price": 2.95, "stock": 18},
]

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hi! How can I help you?"
        }
    ]

with st.sidebar:
    if st.button("Home", key="home_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()

    if st.button("Orders", key="orders_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "orders"
        st.rerun()

json_path_inventory = Path("inventory.json")
if json_path_inventory.exists():
    with open(json_path_inventory, "r") as f:
        inventory = json.load(f)

json_path_orders = Path("orders.json")
if json_path_orders.exists():
    with open(json_path_orders, "r") as f:
        orders = json.load(f)
else:
    orders = []

if st.session_state["page"] == "home":
    col1, col2 = st.columns([4, 2])

    with col1:
        selected_category = st.radio("Select Category", ["Orders", "Inventory"], horizontal=True)

        if selected_category == "Inventory":
            st.markdown("## Inventory")
            if len(inventory) > 0:
                st.dataframe(inventory)
            else:
                st.warning("No item is found.")
        else:
            st.markdown("## Orders")
            if len(orders) > 0:
                st.dataframe(orders)
            else:
                st.warning("No orders are recorded yet.")

    with col2:
        if selected_category == "Inventory":
            st.metric("Total Inventory", f"{len(inventory)} items")
        else:
            st.metric("Total Orders", f"{len(orders)} orders")

elif st.session_state["page"] == "orders":
    tab1, tab2 = st.tabs(["Add New Order", "Cancel Order"])

    with tab1:
        col1, col2 = st.columns([3, 3])

        with col1:
            st.subheader("Add New Order")

            selected_item = st.selectbox(
                "Items",
                options=inventory,
                format_func=lambda x: f"{x['name']}, Stock:{x['stock']}",
                key="inventory_selector"
            )

            quantity = st.number_input("Quantity", min_value=1, step=1)

            if st.button("Create Order", key="create_order_btn", type="primary", use_container_width=True):
                if quantity > selected_item["stock"]:
                    st.error("Not enough stock available.")
                else:
                    total = quantity * selected_item["unit_price"]

                    with st.spinner("Recording the new order..."):
                        for item in inventory:
                            if item["item_id"] == selected_item["item_id"]:
                                item["stock"] = item["stock"] - quantity
                                break

                        orders.append({
                            "id": str(uuid.uuid4()),
                            "item_id": selected_item["item_id"],
                            "quantity": quantity,
                            "status": "Placed",
                            "total": total
                        })

                        with open(json_path_inventory, "w") as f:
                            json.dump(inventory, f)

                        with open(json_path_orders, "w") as f:
                            json.dump(orders, f)

                        st.balloons()
                        time.sleep(2)

                        st.session_state["page"] = "home"
                        st.rerun()

        with col2:
            st.subheader("Chatbot - Ai Assistant")

            col11, col22 = st.columns([3, 1])

            with col11:
                st.caption("Try Asking: How can I add a new order?")

            with col22:
                if st.button("Clear", key="clear_chat_button"):
                    st.session_state["messages"] = [
                        {
                            "role": "assistant",
                            "content": "Hi! How can I help you?"
                        }
                    ]
                    st.rerun()

            with st.container(border=True, height=250):
                for message in st.session_state["messages"]:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

            user_input = st.chat_input("Ask a question...")

            if user_input:
                st.session_state["messages"].append(
                    {
                        "role": "user",
                        "content": user_input
                    }
                )

                with st.spinner("Thinking..."):
                    ai_response = "I could not find an answer for it, try again!"
                    time.sleep(2)

                st.session_state["messages"].append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )

                st.rerun()

    with tab2:
        pass
     