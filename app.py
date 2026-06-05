import streamlit as st
import pandas as pd

# Page configurations
st.set_page_config(page_title="Factory Management System", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Premium Mixed Look & Better Tables (Fixed unsafe_allow_html)
st.markdown("""
    <style>
    .main-title {
        font-size: 26px !important;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 14px !important;
        color: #6B7280;
        margin-bottom: 20px;
    }
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        overflow: hidden;
    }
    div[data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Application Header (Compact and clean - Fixed unsafe_allow_html)
st.markdown("<div class='main-title'>🏭 Production & Wage Management System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>කර්මාන්තශාලා නිෂ්පාදන, දෛනික වැටුප් සහ වියදම් කළමනාකරණ පද්ධතිය</div>", unsafe_allow_html=True)
st.markdown("---")

# Initialize Session States for Data Retention
if 'tasks' not in st.session_state:
    raw_tasks = [
        ('මල් කනු හැදීම', 'Making (හැදීම)'), ('මල් කනු ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), 
        ('මල් කනු වලට කැට ඇල්ලීම', 'Designing (කැට/මල් ඇල්ලීම)'), ('මල් කනු රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), 
        ('මල් කනු පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල් කනු හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල් කනු රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල් කනු පාට කිරීම', 'Painting (පාට කිරීම)'),
        ('මල් කනු පාදන් හැදීම', 'Making (හැදීම)'), ('මල් කනු පාදන් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), 
        ('මල් කනු පාදන් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල් කනු පාදන් හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල් කනු පාදන් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල් කනු පාදන් පාට කිරීම', 'Painting (පාට කිරීම)'),
        ('ටයිල් ප්ලේට් හැදීම', 'Making (හැදීම)'), ('ටයිල් ප්ලේට් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), 
        ('ටයිල් ප්ලේට් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල පොඩි බෝල් හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල පොඩි බෝල් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල්වල පොඩි බෝල් ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), 
        ('වතුර මල්වල පොඩි බෝල් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල ලොකු බෝල් හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල ලොකු බෝල් රෆ් කිරීම', 'Roughing (රෆ් කිරීම)'), ('වතුර මල්වල ලොකු බෝල් ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), 
        ('වතුර මල්වල ලොකු බෝල් පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල ලොකු කැට හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල ලොකු කැට ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), ('වතුර මල්වල ලොකු කැට වලට මල් ඇල්ලීම', 'Designing (කැට/මල් ඇල්ලීම)'), 
        ('වතුර මල්වල ලොකු කැට පාට කිරීම', 'Painting (පාට කිරීම)'), ('වතුර මල්වල පොඩි කැට හැදීම', 'Making (හැදීම)'), 
        ('වතුර මල්වල පොඩි කැට ෆිනිශින් කිරීම', 'Finishing (ෆිනිශින්)'), ('වතුර මල්වල පොඩි කැට වලට මල් ඇල්ලීම', 'Designing (කැට/මල් ඇල්ලීම)'), 
        ('වතුර මල්වල පොඩි කැට පාට කිරීම', 'Painting (පාට කිරීම)'), ('"බුදුසරනයි" කැට හැදීම', 'Making (හැදීම)'), 
        ('"මල්" කැට හැදීම', 'Making (හැදීම)'), ('"කරඩු ඇතා" කැට හැදීම', 'Making (හැදීම)'), ('"දර්ම චක්‍ර" කැට හැදීම', 'Making (හැදීම)')
    ]
    st.session_state.tasks = pd.DataFrame({
        'Task Name (වැඩ කොටස)': [t[0] for t in raw_tasks],
        'Category (කාණ්ඩය)': [t[1] for t in raw_tasks],
        'Piece Rate / ගෙවන මුදල (Rs)': [150.0] * len(raw_tasks)
    })

if 'materials' not in st.session_state:
    st.session_state.materials = pd.DataFrame({
        'Material Name (අමුද්‍රව්‍ය)': ['Cement (සිමෙන්ති) - Bag', 'Steel Rods (කම්බි) - 1kg', 'Sand (වැලි) - Cube', 'Paint (තීන්ත) - 1L'],
        'Unit Price / මිල (Rs)': [2400.0, 320.0, 14000.0, 1800.0]
    })

if 'products' not in st.session_state:
    st.session_state.products = [
        {
            'name': 'මල් කනුව (Style 1)',
            'price': 5000.0,
            'image': None  # Holds bytes or none
        },
        {
            'name': 'වතුර මල් කනුව (Style 1)',
            'price': 8500.0,
            'image': None
        }
    ]

# --- Price Reminder System ---
if 'price_confirmed' not in st.session_state:
    st.session_state.price_confirmed = False

st.sidebar.markdown("### 🔔 System Alerts")
if not st.session_state.price_confirmed:
    st.sidebar.warning("⚠️ කරුණාකර අමුද්‍රව්‍ය මිල ගණන් යාවත්කාලීන දැයි පරීක්ෂා කරන්න. (Please verify material prices)")
    if st.sidebar.button("මිල ගණන් නිවැරදියි (Confirm)"):
        st.session_state.price_confirmed = True
        st.rerun()
else:
    st.sidebar.success("✅ අමුද්‍රව්‍ය මිල ගණන් තහවුරු කර ඇත.")
st.sidebar.markdown("---")

# Sidebar Downward Navigation Menu
st.sidebar.markdown("### 🧭 Navigation Menu")
menu_option = st.sidebar.radio(
    "පද්ධති අංශ තෝරන්න:",
    [
        "🛍️ Products & Showcase (භාණ්ඩ හා මාදිලි)",
        "📋 Piece Rates List (වැඩ කුලී ලේඛනය)",
        "💰 Daily Wage Calculator (දෛනික වැටුප)",
        "📊 Cost & Profit Summary (ලාභ/අලාභ වාර්තා)",
        "⚙️ Control Panel (දත්ත සහ මිල වෙනස් කිරීම)"
    ]
)

# 1. Products & Showcase Section
if menu_option == "🛍️ Products & Showcase (භාණ්ඩ හා මාදිලි)":
    st.markdown("### 🛍️ Product Styles & Selling Prices")
    
    if len(st.session_state.products) == 0:
        st.info("දැනට කිසිදු නිෂ්පාදනයක් ඇතුලත් කර නැත. Control Panel එකෙන් ඇතුලත් කරන්න.")
    else:
        cols = st.columns(3)
        for index, prod in enumerate(st.session_state.products):
            with cols[index % 3]:
                st.markdown(f"##### 📦 {prod['name']}")
                if prod['image'] is not None:
                    st.image(prod['image'], use_container_width=True)
                else:
                    st.warning("No image uploaded for this style.")
                st.write(f"**Selling Price (විකුණුම් මිල):** Rs. {prod['price']:,}")
                st.markdown("---")

# 2. Piece Rates List Section
elif menu_option == "📋 Piece Rates List (වැඩ කුලී ලේඛනය)":
    st.markdown("### 📋 Work Category & Piece Rates")
    
    # Filter by category for easy view
    categories = ['All (සියල්ල)'] + list(st.session_state.tasks['Category (කාණ්ඩය)'].unique())
    selected_cat = st.selectbox("කාණ්ඩය අනුව පෙරන්න (Filter by Category):", categories)
    
    if selected_cat == 'All (සියල්ල)':
        display_df = st.session_state.tasks
    else:
        display_df = st.session_state.tasks[st.session_state.tasks['Category (කාණ්ඩය)'] == selected_cat]
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# 3. Daily Wage Calculator Section
elif menu_option == "💰 Daily Wage Calculator (දෛනික වැටුප)":
    st.markdown("### 💰 Daily Wage Calculation")
    st.write("අද දවසේ සේවකයන් සිදුකළ වැඩ කොටස් සහ ප්‍රමාණයන් තෝරන්න.")
    
    # Filter tasks by operation category to select cleanly
    cat_to_filter = st.selectbox("වැඩ වර්ගය තෝරන්න (Select Work Type):", st.session_state.tasks['Category (කාණ්ඩය)'].unique())
    filtered_tasks_options = st.session_state.tasks[st.session_state.tasks['Category (කාණ්ඩය)'] == cat_to_filter]['Task Name (වැඩ කොටස)'].tolist()
    
    selected_tasks = st.multiselect("සිදුකළ වැඩ කොටස් තෝරන්න (Select Tasks):", filtered_tasks_options)
    
    total_wage = 0
    if selected_tasks:
        st.markdown("#### 🔢 Enter Quantities (ප්‍රමාණයන් ඇතුලත් කරන්න)")
        for task in selected_tasks:
            col1, col2, col3 = st.columns([2, 1, 1])
            task_row = st.session_state.tasks[st.session_state.tasks['Task Name (වැඩ කොටස)'] == task].iloc[0]
            task_price = task_row['Piece Rate / ගෙවන මුදල (Rs)']
            
            with col1:
                st.write(f"**{task}** ({task_row['Category (කාණ්ඩය)']})")
                st.caption(f"Rate: Rs. {task_price}")
            with col2:
                qty = st.number_input(f"Quantity for {task}", min_value=1, value=1, key=f"wage_qty_{task}")
            with col3:
                line_total = task_price * qty
                st.write(f"**Total: Rs. {line_total:,}**")
                total_wage += line_total
                
        st.markdown("---")
        st.subheader(f"💵 Total Daily Wage Payable (මුළු දෛනික වැටුප): Rs. {total_wage:,}")

# 4. Cost & Profit Summary Section
elif menu_option == "📊 Cost & Profit Summary (ලාභ/අලාභ වාර්තා)":
    st.markdown("### 📊 Production Cost & Profit Calculation")
    
    if len(st.session_state.products) == 0:
        st.warning("කරුණාකර ප්‍රථමයෙන් භාණ්ඩයක් ඇතුලත් කරන්න.")
    else:
        product_names = [p['name'] for p in st.session_state.products]
        selected_product_name = st.selectbox("නිෂ්පාදිත භාණ්ඩය තෝරන්න (Select Product):", product_names)
        
        # Get selected product details
        prod_obj = next(p for p in st.session_state.products if p['name'] == selected_product_name)
        selling_price = prod_obj['price']
        
        st.write(f"**Selling Price (විකුණුම් මිල):** Rs. {selling_price:,}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🛠️ 1. Labor Costs (වැඩ කුලී වියදම)")
            cost_tasks = st.multiselect("මෙම කණුව/භාණ්ඩය සෑදීමට අදාළ වැඩ කොටස් තෝරන්න:", st.session_state.tasks['Task Name (වැඩ කොටස)'])
            
            total_labor_cost = 0
            for task in cost_tasks:
                task_price = st.session_state.tasks[st.session_state.tasks['Task Name (වැඩ කොටස)'] == task].iloc[0]['Piece Rate / ගෙවන මුදල (Rs)']
                qty = st.number_input(f"කෑලි ගණන ({task})", min_value=1, value=1, key=f"cost_calc_qty_{task}")
                total_labor_cost += (task_price * qty)
                
        with col2:
            st.markdown("##### 🧱 2. Material Costs (අමුද්‍රව්‍ය වියදම)")
            selected_materials = st.multiselect("භාවිතා කල අමුද්‍රව්‍ය තෝරන්න:", st.session_state.materials['Material Name (අමුද්‍රව්‍ය)'].tolist())
            
            total_material_cost = 0
            for mat in selected_materials:
                mat_price = st.session_state.materials[st.session_state.materials['Material Name (අමුද්‍රව්‍ය)'] == mat].iloc[0]['Unit Price / මිල (Rs)']
                mat_qty = st.number_input(f"ප්‍රමාණය ({mat})", min_value=0.0, value=1.0, step=0.1, key=f"mat_qty_{mat}")
                total_material_cost += (mat_price * mat_qty)
                
        total_production_cost = total_labor_cost + total_material_cost
        profit = selling_price - total_production_cost
        
        st.markdown("---")
        st.markdown("#### 📋 Cost Breakdown & Summary")
        
        summary_data = {
            "Description": ["Selling Price (විකුණුම් මිල)", "Total Labor Cost (මුළු වැඩ කුලිය)", "Total Material Cost (මුළු අමුද්‍රව්‍ය වියදම)", "Total Production Cost (සම්පූර්ණ නිෂ්පාදන වියදම)"],
            "Amount (Rs)": [selling_price, total_labor_cost, total_material_cost, total_production_cost]
        }
        st.table(pd.DataFrame(summary_data))
        
        if profit >= 0:
            st.success(f"📈 Net Profit per Unit (ශුද්ධ ලාභය): Rs. {profit:,}")
        else:
            st.error(f"📉 Net Loss per Unit (අලාභය): Rs. {profit:,}")

# 5. Control Panel Section
elif menu_option == "⚙️ Control Panel (දත්ත සහ මිල වෙනස් කිරීම)":
    st.markdown("### ⚙️ Factory Data Control Panel")
    st.write("ඇප් එකේ ඇති සියලුම දත්ත මෙතනින් වෙනස් කර සේව් කළ හැක.")
    
    # Section A: Manage Product Styles with Gallery Upload
    st.markdown("---")
    st.markdown("#### 📸 Manage Product Styles & Photo Upload")
    
    # Display Current Styles and allow deletion
    if len(st.session_state.products) > 0:
        st.write("**දැනට පවතින මාදිලි (Current Styles):**")
        for i, p in enumerate(st.session_state.products):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"**{p['name']}** - Rs. {p['price']:,}")
            with c2:
                if p['image'] is not None:
                    st.caption("✅ Photo Loaded")
                else:
                    st.caption("❌ No Photo")
            with c3:
                if st.button("Delete", key=f"del_prod_{i}"):
                    st.session_state.products.pop(i)
                    st.rerun()
                    
    # Form to add new Product Style with File Uploader
    with st.form("add_product_form", clear_on_submit=True):
        st.write("**➕ Add New Style / Product Model**")
        new_name = st.text_input("Product Name (නිෂ්පාදනයේ නම):")
        new_price = st.number_input("Selling Price (විකුණුම් මිල රු.):", min_value=0.0, value=1000.0)
        uploaded_file = st.file_uploader("Upload Photo from Gallery (පින්තූරය තෝරන්න):", type=["jpg", "png", "jpeg"])
        
        submit_product = st.form_submit_button("Save New Product Style")
        if submit_product:
            if new_name:
                img_data = None
                if uploaded_file is not None:
                    img_data = uploaded_file.read()
                
                st.session_state.products.append({
                    'name': new_name,
                    'price': new_price,
                    'image': img_data
                })
                st.success(f"'{new_name}' සාර්ථකව පද්ධතියට එකතු කරන ලදී!")
                st.rerun()
            else:
                st.error("කරුණාකර නිෂ්පාදනයේ නම ඇතුලත් කරන්න.")

    # Section B: Manage Piece Rates
    st.markdown("---")
    st.markdown("#### 📋 Update Piece Rates (වැඩ කුලී මිල ගණන් වෙනස් කිරීම)")
    st.write("වගුවේ ඇති ඕනෑම අගයක් වෙනස් කර පහත 'Save Piece Rates' බොත්තම ඔබන්න. අලුත් වැඩ කොටස් වගුවේ අන්තිම පේළියෙන් එක් කළ හැක.")
    edited_tasks = st.data_editor(st.session_state.tasks, num_rows="dynamic", use_container_width=True)
    if st.button("Save Piece Rates (වැඩ කුලිය සේව් කරන්න)"):
        st.session_state.tasks = edited_tasks
        st.success("වැඩ කුලී මිල ගණන් සාර්ථකව යාවත්කාලීන කරන ලදී!")
        st.rerun()

    # Section C: Manage Material Prices
    st.markdown("---")
    st.markdown("#### 🧱 Update Material Prices (අමුද්‍රව්‍ය මිල ගණන් වෙනස් කිරීම)")
    st.write("සිමෙන්ති, කම්බි ඇතුළු අමුද්‍රව්‍ය වල මිල ගණන් වෙනස් කිරීමට හෝ අලුත් ඒවා ඇතුලත් කිරීමට මෙම වගුව භාවිතා කරන්න.")
    
    edited_materials = st.data_editor(st.session_state.materials, num_rows="dynamic", use_container_width=True)
    if st.button("Save Material Prices (අමුද්‍රව්‍ය මිල සේව් කරන්න)"):
        st.session_state.materials = edited_materials
        st.session_state.price_confirmed = True 
        st.success("අමුද්‍රව්‍ය මිල ගණන් සාර්ථකව යාවත්කාලීන කරන ලදී!")
        st.rerun()
