import streamlit as st
import pandas as pd

# පිටුවේ සැකසුම්
st.set_page_config(page_title="කර්මාන්තශාලා කළමනාකරණ පද්ධතිය", layout="wide")

st.title("🏭 නිෂ්පාදන සහ වැටුප් කළමනාකරණ පද්ධතිය")
st.markdown("---")

# ඇප් එක refresh වෙද්දි දත්ත මැකී නොයන්න Session State භාවිතය
if 'tasks' not in st.session_state:
    # ඔබ ලබා දුන් සියලුම වැඩ කොටස්
    task_list = [
        'මල් කනු හැදීම', 'මල් කනු ෆිනිශින් කිරීම', 'මල් කනු වලට කැට ඇල්ලීම', 'මල් කනු රෆ් කිරීම', 'මල් කනු පාට කිරීම',
        'වතුර මල් කනු හැදීම', 'වතුර මල් කනු රෆ් කිරීම', 'වතුර මල් කනු පාට කිරීම',
        'මල් කනු පාදන් හැදීම', 'මල් කනු පාදන් රෆ් කිරීම', 'මල් කනු පාදන් පාට කිරීම',
        'වතුර මල් කනු පාදන් හැදීම', 'වතුර මල් කනු පාදන් රෆ් කිරීම', 'වතුර මල් කනු පාදන් පාට කිරීම',
        'ටයිල් ප්ලේට් හැදීම', 'ටයිල් ප්ලේට් රෆ් කිරීම', 'ටයිල් ප්ලේට් පාට කිරීම',
        'වතුර මල්වල පොඩි බෝල් හැදීම', 'වතුර මල්වල පොඩි බෝල් රෆ් කිරීම', 'වතුර මල්වල පොඩි බෝල් ෆිනිශින් කිරීම', 'වතුර මල්වල පොඩි බෝල් පාට කිරීම',
        'වතුර මල්වල ලොකු බෝල් හැදීම', 'වතුර මල්වල ලොකු බෝල් රෆ් කිරීම', 'වතුර මල්වල ලොකු බෝල් ෆිනිශින් කිරීම', 'වතුර මල්වල ලොකු බෝල් පාට කිරීම',
        'වතුර මල්වල ලොකු කැට හැදීම', 'වතුර මල්වල ලොකු කැට ෆිනිශින් කිරීම', 'වතුර මල්වල ලොකු කැට වලට මල් ඇල්ලීම', 'වතුර මල්වල ලොකු කැට පාට කිරීම',
        'වතුර මල්වල පොඩි කැට හැදීම', 'වතුර මල්වල පොඩි කැට ෆිනිශින් කිරීම', 'වතුර මල්වල පොඩි කැට වලට මල් ඇල්ලීම', 'වතුර මල්වල පොඩි කැට පාට කිරීම',
        '"බුදුසරනයි" කැට හැදීම', '"මල්" කැට හැදීම', '"කරඩු ඇතා" කැට හැදීම', '"දර්ම චක්‍ර" කැට හැදීම'
    ]
    
    # දැනට තාවකාලික මිල ගණන් (රුපියල් 100 බැගින්) දමා ඇත. ඔබට පසුව මෙය ඇප් එකෙන් වෙනස් කළ හැක.
    initial_prices = [100.0] * len(task_list)
    
    st.session_state.tasks = pd.DataFrame({
        'වැඩ කොටස': task_list,
        'ගෙවන මුදල (රු)': initial_prices
    })

if 'products' not in st.session_state:
    # තාවකාලික කණු Styles කීපයක්
    st.session_state.products = pd.DataFrame({
        'නිෂ්පාදනය (Style)': ['මල් කනුව (Style 1)', 'වතුර මල් කනුව (Style 1)'],
        'විකුණන මිල (රු)': [5000.0, 8500.0],
        'පින්තූරය (URL)': ['https://via.placeholder.com/200?text=Style+1', 'https://via.placeholder.com/200?text=Water+Fountain']
    })

# Tabs නිර්මාණය කිරීම
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛍️ භාණ්ඩ හා මිල ගණන්", 
    "📋 වැඩ කුලිය (Piece Rates)", 
    "💰 දෛනික වැටුප ගණනය", 
    "📊 වියදම් සහ ලාභය", 
    "⚙️ දත්ත වෙනස් කිරීම"
])

# 1. භාණ්ඩ හා මිල ගණන් Tab එක
with tab1:
    st.header("නිෂ්පාදන මාදිලි (Styles) සහ විකුණුම් මිල")
    cols = st.columns(3)
    for index, row in st.session_state.products.iterrows():
        with cols[index % 3]:
            st.image(row['පින්තූරය (URL)'], use_container_width=True)
            st.subheader(row['නිෂ්පාදනය (Style)'])
            st.write(f"**විකුණන මිල:** රු. {row['විකුණන මිල (රු)']}")
            st.markdown("---")

# 2. වැඩ කුලිය Tab එක
with tab2:
    st.header("එක් එක් කොටස සඳහා ගෙවන මුදල්")
    st.dataframe(st.session_state.tasks, use_container_width=True, hide_index=True)

# 3. දෛනික වැටුප ගණනය Tab එක
with tab3:
    st.header("දෛනික වැටුප් ගණනය කිරීම")
    st.write("අද දවසේ සිදුකළ වැඩ කොටස් සහ ප්‍රමාණයන් තෝරන්න.")
    
    selected_tasks = st.multiselect("සිදුකළ වැඩ කොටස් තෝරන්න:", st.session_state.tasks['වැඩ කොටස'])
    
    total_wage = 0
    if selected_tasks:
        for task in selected_tasks:
            col1, col2, col3 = st.columns([2, 1, 1])
            task_price = st.session_state.tasks.loc[st.session_state.tasks['වැඩ කොටස'] == task, 'ගෙවන මුදල (රු)'].values[0]
            
            with col1:
                st.write(f"**{task}** (රු. {task_price} බැගින්)")
            with col2:
                qty = st.number_input(f"ප්‍රමාණය ({task})", min_value=1, value=1, key=f"qty_{task}")
            with col3:
                line_total = task_price * qty
                st.write(f"මුදල: රු. {line_total}")
                total_wage += line_total
                
        st.markdown("---")
        st.subheader(f"අද දින ගෙවිය යුතු මුළු වැටුප: රු. {total_wage}")

# 4. වියදම් සහ ලාභය Tab එක
with tab4:
    st.header("නිෂ්පාදන වියදම සහ ලාභය ගණනය")
    selected_product = st.selectbox("නිෂ්පාදනය තෝරන්න:", st.session_state.products['නිෂ්පාදනය (Style)'])
    
    if selected_product:
        selling_price = st.session_state.products.loc[st.session_state.products['නිෂ්පාදනය (Style)'] == selected_product, 'විකුණන මිල (රු)'].values[0]
        st.write(f"**මෙම භාණ්ඩයේ විකුණුම් මිල:** රු. {selling_price}")
        
        st.write("මෙම කණුව සෑදීම සඳහා ගිය වැඩ කොටස් තෝරන්න (වියදම බැලීමට):")
        cost_tasks = st.multiselect("අදාළ වැඩ කොටස්:", st.session_state.tasks['වැඩ කොටස'], key="cost_tasks")
        
        total_cost = 0
        material_cost = st.number_input("අමුද්‍රව්‍ය සඳහා ගිය වියදම (රු.)", min_value=0.0, value=0.0)
        
        if cost_tasks:
            for task in cost_tasks:
                task_price = st.session_state.tasks.loc[st.session_state.tasks['වැඩ කොටස'] == task, 'ගෙවන මුදල (රු)'].values[0]
                qty = st.number_input(f"කෑලි ගණන ({task})", min_value=1, value=1, key=f"cost_qty_{task}")
                total_cost += (task_price * qty)
                
        total_production_cost = total_cost + material_cost
        profit = selling_price - total_production_cost
        
        st.markdown("---")
        st.write(f"**වැඩ කුලී වියදම:** රු. {total_cost}")
        st.write(f"**අමුද්‍රව්‍ය වියදම:** රු. {material_cost}")
        st.subheader(f"සම්පූර්ණ වියදම (Cost): රු. {total_production_cost}")
        
        if profit >= 0:
            st.success(f"ආයතනයේ ලාභය (Profit): රු. {profit}")
        else:
            st.error(f"අලාභය (Loss): රු. {profit}")

# 5. දත්ත කළමනාකරණය Tab එක
with tab5:
    st.header("දත්ත සහ මිල ගණන් යාවත්කාලීන කිරීම (Update)")
    
    st.subheader("වැඩ කුලිය වෙනස් කරන්න")
    edited_tasks = st.data_editor(st.session_state.tasks, num_rows="dynamic", use_container_width=True)
    if st.button("වැඩ කුලිය Save කරන්න"):
        st.session_state.tasks = edited_tasks
        st.success("සාර්ථකව යාවත්කාලීන කරන ලදී!")

    st.markdown("---")
    st.subheader("අලුත් Styles සහ පින්තූර ඇතුලත් කරන්න")
    st.write("වෙනස් කිරීමට වගුවේ ඇති දත්ත මත Click කරන්න. අලුත් ඒවා එකතු කිරීමට පහලින් type කරන්න. පින්තූර සඳහා පින්තූරයේ Link (URL) එක ඇතුලත් කරන්න.")
    edited_products = st.data_editor(st.session_state.products, num_rows="dynamic", use_container_width=True)
    if st.button("Styles Save කරන්න"):
        st.session_state.products = edited_products
        st.success("Styles සාර්ථකව යාවත්කාලීන කරන ලදී!")
