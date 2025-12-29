# app.py - Main Streamlit Application
import streamlit as st
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="Marketing Strategy Decision Tool",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'product_type' not in st.session_state:
    st.session_state.product_type = None
if 'product_stage' not in st.session_state:
    st.session_state.product_stage = None
if 'market_type' not in st.session_state:
    st.session_state.market_type = None
if 'segmentation' not in st.session_state:
    st.session_state.segmentation = []
if 'competitive_forces' not in st.session_state:
    st.session_state.competitive_forces = {}
if 'distribution_config' not in st.session_state:
    st.session_state.distribution_config = {'customization': None, 'market_concentration': None}
if 'selected_channel' not in st.session_state:
    st.session_state.selected_channel = None

# Data definitions
PRODUCT_TYPES = {
    'fmcg': {'name': 'FMCG/Consumer Goods', 'desc': 'Fast-moving consumer products'},
    'luxury': {'name': 'Luxury Products', 'desc': 'Premium, high-differentiation items'},
    'electronics': {'name': 'Electronics/Gadgets', 'desc': 'Technology products'},
    'service': {'name': 'Service', 'desc': 'Intangible offerings'}
}

PRODUCT_STAGES = ['Introduction', 'Growth', 'Maturity', 'Decline']

MARKET_TYPES = {
    'new-new': {'name': 'New Market + New Product', 'strategy': 'Diversification'},
    'new-existing': {'name': 'New Market + Existing Product', 'strategy': 'Market Development'},
    'existing-new': {'name': 'Existing Market + New Product', 'strategy': 'Product Development'},
    'existing-existing': {'name': 'Existing Market + Existing Product', 'strategy': 'Market Penetration'}
}

SEGMENTATION_OPTIONS = {
    'user-status': {'name': 'User Status', 'desc': 'Non-users, potential users, regular users'},
    'usage-rate': {'name': 'Usage Rate', 'desc': 'Light, medium, heavy users'},
    'loyalty': {'name': 'Loyalty', 'desc': 'Brand loyal, switchers, competitors'},
    'attitude': {'name': 'Attitude', 'desc': 'Enthusiastic, positive, negative'},
    'demographic': {'name': 'Demographic', 'desc': 'Age, income, education, family size'},
    'psychographic': {'name': 'Psychographic', 'desc': 'Lifestyle, values, personality'}
}

DISTRIBUTION_CHANNELS = {
    'high-concentrated': {
        'name': 'Direct Distribution',
        'model': 'VMS (Vertical Marketing System)',
        'description': 'Direct sales to concentrated customer base',
        'pros': ['Perfect control over placement and quality', 'Enhanced consumer satisfaction', 'Less response time to grievances'],
        'cons': ['Requires huge investments', 'May not be viable for low-margin products', 'Potential loss of flexibility'],
        'examples': ['Company-owned stores', 'Direct sales force', 'E-commerce platform', 'B2B direct sales']
    },
    'high-fragmented': {
        'name': 'Franchise Operations',
        'model': 'Hybrid VMS',
        'description': 'Standardized operations through franchise network',
        'pros': ['Rapid market expansion', 'Controlled brand experience', 'Shared investment with franchisees', 'Local market expertise'],
        'cons': ['Franchisee management complexity', 'Quality control challenges', 'Profit sharing with franchisees'],
        'examples': ['Fast food franchises', 'Retail chain franchises', 'Service franchises', 'Master franchise model']
    },
    'low-concentrated': {
        'name': 'Distribution + Personal Selling',
        'model': 'Hybrid Traditional',
        'description': 'Selected distributors with sales force support',
        'pros': ['Market access without heavy investment', 'Sales force ensures customer relationships', 'Flexibility in market coverage'],
        'cons': ['Moderate control over distribution', 'Coordination complexity', 'Channel conflict potential'],
        'examples': ['Industrial distributors', 'B2B dealers with sales support', 'Authorized dealers', 'Value-added resellers']
    },
    'low-fragmented': {
        'name': 'Third-Party Intensive Distribution',
        'model': 'Traditional Channel',
        'description': 'Maximum market coverage through multiple retailers',
        'pros': ['Better market access by appointing more retailers', 'Low investment in distribution', 'Wide availability'],
        'cons': ['Focus on volume, not customer satisfaction', 'Slow information flow', 'Manufacturer has minimal or no control', 'Frequent conflicts among channel members'],
        'examples': ['Mass retailers', 'Supermarkets', 'Online marketplaces', 'Wholesaler networks', 'Multi-brand outlets']
    }
}

def get_distribution_recommendation():
    config = st.session_state.distribution_config
    if not config['customization'] or not config['market_concentration']:
        return None
    key = f"{config['customization']}-{config['market_concentration']}"
    return DISTRIBUTION_CHANNELS.get(key)

def get_recommendations():
    recommendations = {
        'strategy': '',
        'pricing': '',
        'promotion': '',
        'distribution': '',
        'messaging': []
    }
    
    # Ansoff Matrix Strategy
    if st.session_state.market_type:
        recommendations['strategy'] = MARKET_TYPES[st.session_state.market_type]['strategy']
    
    # PLC-based recommendations
    stage = st.session_state.product_stage
    if stage == 'Introduction':
        recommendations['promotion'] = 'Focus on Information & Advertising to build awareness. Use promotion to induce trial. Less sales promotion, more advertising investment.'
        recommendations['pricing'] = 'Penetration pricing (low to gain market share) or Skimming pricing (high for innovative products)'
    elif stage == 'Growth':
        recommendations['promotion'] = 'Increase advertising to build preference. Sales promotions to attract new consumers and increase consumption.'
        recommendations['pricing'] = 'Maintain or slightly reduce prices to match competition and maximize market share'
    elif stage == 'Maturity':
        recommendations['promotion'] = 'Effort to induce different usages. More sales promotion, less advertising. Focus on attracting marginal customers and brand switching.'
        recommendations['pricing'] = 'Competitive pricing, promotional pricing to defend market share'
    elif stage == 'Decline':
        recommendations['promotion'] = 'Frequent sales promotions to liquidate stock. Extremely low advertising spend. Minimal promotional investment.'
        recommendations['pricing'] = 'Discount pricing to clear inventory, harvest profits'
    
    # Distribution
    dist_rec = get_distribution_recommendation()
    if dist_rec:
        recommendations['distribution'] = f"{dist_rec['name']} - {dist_rec['description']}"
    else:
        recommendations['distribution'] = 'Complete distribution configuration to get recommendation'
    
    # Competitive forces messaging
    forces = st.session_state.competitive_forces
    if forces.get('rivalry') == 'High':
        recommendations['messaging'].append('Differentiate strongly - high rivalry requires clear positioning')
    if forces.get('buyers') == 'High':
        recommendations['messaging'].append('Focus on value proposition - buyers have strong bargaining power')
    if forces.get('newEntrants') == 'High':
        recommendations['messaging'].append('Build brand loyalty quickly - threat of new entrants is high')
    if forces.get('substitutes') == 'High':
        recommendations['messaging'].append('Emphasize unique benefits - substitutes pose a threat')
    
    # Product type messaging
    product_type = st.session_state.product_type
    if product_type == 'luxury':
        recommendations['messaging'].append('Premium positioning, emotional branding, exclusivity messaging')
    elif product_type == 'fmcg':
        recommendations['messaging'].append('Mass market appeal, convenience, value for money')
    elif product_type == 'electronics':
        recommendations['messaging'].append('Innovation focus, feature benefits, early adopter targeting')
    
    # Segmentation messaging
    if 'loyalty' in st.session_state.segmentation:
        recommendations['messaging'].append('Implement loyalty programs and retention marketing')
    if 'usage-rate' in st.session_state.segmentation:
        recommendations['messaging'].append('Tailor messaging for heavy vs. light users differently')
    if 'psychographic' in st.session_state.segmentation:
        recommendations['messaging'].append('Create lifestyle-based campaigns aligned with values')
    
    return recommendations

def generate_whatsapp_message():
    channel = get_distribution_recommendation()
    product_name = PRODUCT_TYPES[st.session_state.product_type]['name'] if st.session_state.product_type else ''
    
    message = f"""Hi! I'd like to discuss distribution channel setup:

Product Type: {product_name}
Product Stage: {st.session_state.product_stage}
Recommended Channel: {channel['name'] if channel else ''}
Channel Model: {channel['model'] if channel else ''}
Selected Option: {st.session_state.selected_channel or ''}

I'm interested in learning more about implementation."""
    
    return f"https://wa.me/?text={urllib.parse.quote(message)}"

# Title
st.title("📊 Marketing Strategy Decision Tool")
st.markdown("*Data-driven marketing decisions using proven frameworks*")

# Progress bar
progress = (st.session_state.step - 1) / 5
st.progress(progress)

# Step indicator
cols = st.columns(6)
step_names = ['Product', 'Market', 'Segments', 'Forces', 'Distribution', 'Results']
for i, (col, name) in enumerate(zip(cols, step_names), 1):
    with col:
        if i < st.session_state.step:
            st.markdown(f"**✓ {name}**")
        elif i == st.session_state.step:
            st.markdown(f"**→ {name}**")
        else:
            st.markdown(f"{name}")

st.markdown("---")

# Step 1: Product Information
if st.session_state.step == 1:
    st.header("Step 1: Product Information")
    st.markdown("Select your product type and lifecycle stage")
    
    st.subheader("Product Type")
    cols = st.columns(2)
    for i, (key, value) in enumerate(PRODUCT_TYPES.items()):
        with cols[i % 2]:
            if st.button(f"**{value['name']}**\n\n{value['desc']}", key=f"prod_{key}", use_container_width=True):
                st.session_state.product_type = key
    
    if st.session_state.product_type:
        st.success(f"Selected: {PRODUCT_TYPES[st.session_state.product_type]['name']}")
    
    st.subheader("Product Lifecycle Stage")
    cols = st.columns(4)
    for i, stage in enumerate(PRODUCT_STAGES):
        with cols[i]:
            if st.button(stage, key=f"stage_{stage}", use_container_width=True):
                st.session_state.product_stage = stage
    
    if st.session_state.product_stage:
        st.success(f"Selected: {st.session_state.product_stage}")

# Step 2: Market Strategy
elif st.session_state.step == 2:
    st.header("Step 2: Market Strategy (Ansoff Matrix)")
    st.markdown("Choose your market-product combination")
    
    cols = st.columns(2)
    for i, (key, value) in enumerate(MARKET_TYPES.items()):
        with cols[i % 2]:
            if st.button(f"**{value['name']}**\n\nStrategy: {value['strategy']}", key=f"market_{key}", use_container_width=True):
                st.session_state.market_type = key
    
    if st.session_state.market_type:
        st.success(f"Selected: {MARKET_TYPES[st.session_state.market_type]['strategy']}")

# Step 3: Customer Segmentation
elif st.session_state.step == 3:
    st.header("Step 3: Customer Segmentation")
    st.markdown("Select relevant segmentation criteria for targeting")
    
    for key, value in SEGMENTATION_OPTIONS.items():
        checked = st.checkbox(f"**{value['name']}** - {value['desc']}", value=key in st.session_state.segmentation, key=f"seg_{key}")
        if checked and key not in st.session_state.segmentation:
            st.session_state.segmentation.append(key)
        elif not checked and key in st.session_state.segmentation:
            st.session_state.segmentation.remove(key)
    
    if st.session_state.segmentation:
        st.success(f"Selected {len(st.session_state.segmentation)} segmentation criteria")

# Step 4: Competitive Forces
elif st.session_state.step == 4:
    st.header("Step 4: Porter's 5 Forces Analysis")
    st.markdown("Assess competitive forces in your market")
    
    forces = [
        ('rivalry', 'Existing Rivalry Between Firms'),
        ('suppliers', 'Bargaining Power of Suppliers'),
        ('buyers', 'Bargaining Power of Customers'),
        ('newEntrants', 'Threat of New Entrants'),
        ('substitutes', 'Threat of Substitutes')
    ]
    
    for key, label in forces:
        st.subheader(label)
        cols = st.columns(3)
        for i, option in enumerate(['Low', 'Medium', 'High']):
            with cols[i]:
                if st.button(option, key=f"force_{key}_{option}", use_container_width=True):
                    st.session_state.competitive_forces[key] = option
        
        if key in st.session_state.competitive_forces:
            st.info(f"Selected: {st.session_state.competitive_forces[key]}")

# Step 5: Distribution Channel
elif st.session_state.step == 5:
    st.header("Step 5: Distribution Channel Strategy")
    st.markdown("Configure your distribution approach")
    
    st.info("**Distribution Channel Selection Framework**\n\nChoose based on product customization level and target market concentration")
    
    st.subheader("Product Customization Level")
    cols = st.columns(2)
    with cols[0]:
        if st.button("**High Customization**\n\nTailored products, bespoke services", key="cust_high", use_container_width=True):
            st.session_state.distribution_config['customization'] = 'high'
    with cols[1]:
        if st.button("**Low Customization**\n\nStandardized products, mass market", key="cust_low", use_container_width=True):
            st.session_state.distribution_config['customization'] = 'low'
    
    if st.session_state.distribution_config['customization']:
        st.success(f"Selected: {st.session_state.distribution_config['customization'].title()} Customization")
    
    st.subheader("Target Market Concentration")
    cols = st.columns(2)
    with cols[0]:
        if st.button("**Concentrated Market**\n\nFew large customers, B2B, niche segments", key="market_conc", use_container_width=True):
            st.session_state.distribution_config['market_concentration'] = 'concentrated'
    with cols[1]:
        if st.button("**Fragmented Market**\n\nMany small customers, B2C, mass market", key="market_frag", use_container_width=True):
            st.session_state.distribution_config['market_concentration'] = 'fragmented'
    
    if st.session_state.distribution_config['market_concentration']:
        st.success(f"Selected: {st.session_state.distribution_config['market_concentration'].title()} Market")
    
    # Show recommendation if config is complete
    channel = get_distribution_recommendation()
    if channel:
        st.markdown("---")
        st.success("### 🎯 Recommended Distribution Channel")
        st.markdown(f"## {channel['name']}")
        st.markdown(f"**Model:** {channel['model']}")
        st.markdown(channel['description'])
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**✓ Pros:**")
            for pro in channel['pros']:
                st.markdown(f"- {pro}")
        with cols[1]:
            st.markdown("**⚠ Cons:**")
            for con in channel['cons']:
                st.markdown(f"- {con}")
        
        st.subheader("Select Specific Channel Type")
        st.session_state.selected_channel = st.selectbox(
            "Choose a channel option:",
            [''] + channel['examples'],
            index=0 if not st.session_state.selected_channel else channel['examples'].index(st.session_state.selected_channel) + 1 if st.session_state.selected_channel in channel['examples'] else 0
        )
        
        if st.session_state.selected_channel:
            if st.button("📱 Book Channel Setup via WhatsApp", use_container_width=True, type="primary"):
                whatsapp_url = generate_whatsapp_message()
                st.markdown(f"[Click here to open WhatsApp]({whatsapp_url})")

# Step 6: Results
elif st.session_state.step == 6:
    st.header("Complete Marketing Recommendations")
    st.markdown("Strategic recommendations based on your inputs")
    
    recommendations = get_recommendations()
    
    st.success(f"### 🎯 Core Strategy: {recommendations['strategy']}")
    
    cols = st.columns(2)
    with cols[0]:
        st.info("### 📈 Promotion Strategy")
        st.markdown(recommendations['promotion'])
    with cols[1]:
        st.info("### 💰 Pricing Strategy")
        st.markdown(recommendations['pricing'])
    
    st.info("### 📦 Distribution Strategy")
    st.markdown(recommendations['distribution'])
    
    if st.session_state.selected_channel:
        st.markdown(f"**Selected Channel:** {st.session_state.selected_channel}")
        if st.button("📱 Contact via WhatsApp", key="whatsapp_final"):
            whatsapp_url = generate_whatsapp_message()
            st.markdown(f"[Click here to open WhatsApp]({whatsapp_url})")
    
    st.warning("### 💡 Key Messaging Insights")
    for msg in recommendations['messaging']:
        st.markdown(f"- {msg}")
    
    st.caption("*Note: These recommendations are based on established marketing frameworks including Consumer Behavior Model (Engel, Blackwell, Miniard & Harcourt 2001), Porter's 5 Forces, Ansoff Matrix, Product Lifecycle, and Distribution Channel Strategy.*")

# Navigation buttons
st.markdown("---")
cols = st.columns([1, 1])

with cols[0]:
    if st.session_state.step > 1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.step -= 1
            st.rerun()

with cols[1]:
    can_proceed = False
    if st.session_state.step == 1:
        can_proceed = st.session_state.product_type and st.session_state.product_stage
    elif st.session_state.step == 2:
        can_proceed = st.session_state.market_type
    elif st.session_state.step == 3:
        can_proceed = len(st.session_state.segmentation) > 0
    elif st.session_state.step == 4:
        can_proceed = len(st.session_state.competitive_forces) == 5
    elif st.session_state.step == 5:
        can_proceed = st.session_state.distribution_config['customization'] and st.session_state.distribution_config['market_concentration']
    
    if st.session_state.step < 6:
        if st.button("Next →", disabled=not can_proceed, use_container_width=True, type="primary"):
            st.session_state.step += 1
            st.rerun()
    else:
        if st.button("🔄 Start New Analysis", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
